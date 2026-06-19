"""
Views for orders.

Provides views for accommodating HTTP requests.
"""

from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from dining_table.models import Table, Bill
from .models import Order
from .serializers import OrderSerializer, OrderPatchSerializer


class OrderView(APIView):
    """Viewset for managing orders."""

    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    PAGINATION_PAGE_SIZE = 1

    def get_order_based_on_permissions(self, request, order_id, table_id=None):
        """
        Returns order from order_id after checking permissions.

        Used by patch() and delete()
        """
        if request.user.is_superuser and request.user.is_staff:
            return get_object_or_404(Order, pk=order_id)
        if table_id is None:
            raise Http404("table_id not found.")
        bill = get_object_or_404(Table, pk=table_id).bills.filter(active=True).first()
        if bill is None:
            raise Http404("No active bill for this table. Contact staff.")
        return get_object_or_404(bill.orders, pk=order_id)

    def get(self, request, table_id=None, bill_id=None, status=None, order_id=None):
        """
        Returns Orders as JSON epending on the passed arguments.

        - If order_id is present:
            > If order_id is valid: returns the required order.
            > If order_id is invalid: raises HTTP 404.
        - If order_id is absent and status is present:
            > If the user is not staff: Raises HTTP 403.
            > If the user is staff:
                >> If status is invalid: Raises HTTP 404.
                >> If status is valid: Returns all orders of passed status in a paginated manner.
        - If order_id and status are absent and table_id is present:
            > If table_id is invalid: Raises HTTP 404.
            > If table_id is valid:
                >> If that table has no active bill: Raises HTTP 404.
                >> If table has an active bill: Returns all orders in that bill.
        - If order_id, status, and table_id are absent and bill_id is present:
            > If bill_id is invalid: raises HTTP 404.
            > If bill_id is valid: returns all orders in the mentioned bill_id.
        - If all parameters are absent:
            > If user is a superuser: Returns all orders in a paginated manner.
            > If user is not a superuser: Raises HTTP 403.
        """
        paginator = self.pagination_class()
        paginator.page_size = self.PAGINATION_PAGE_SIZE

        if order_id is not None:
            order = get_object_or_404(Order, pk=order_id)
            order_data = OrderSerializer(order).data
            return Response(order_data)
        
        if status is not None:
            if not request.user.is_staff:
                raise PermissionDenied("This request is only available to staff.")
            if status.upper() not in ["O", "W", "D"]:
                raise Http404("Invalid status entered.")
            status_orders = Order.objects.filter(status=status.upper())
            status_orders_page = paginator.paginate_queryset(status_orders, request)
            status_orders_data = OrderSerializer(status_orders_page, many=True).data
            return paginator.get_paginated_response(status_orders_data)

        if table_id is not None:
            table = get_object_or_404(Table, pk=table_id)
            bill = table.bills.filter(active=True).first()
            if bill is None:
                raise Http404("No active bill exists for this table.")
            bill_id = bill.pk

        if bill_id is not None:
            bill = get_object_or_404(Bill, pk=bill_id)
            orders = bill.orders.all()
            orders_data = OrderSerializer(orders, many=True).data
            return Response(orders_data)

        if request.user.is_staff and request.user.is_superuser:
            all_orders = Order.objects.all()
            all_orders_page = paginator.paginate_queryset(all_orders, request)
            all_orders_data = OrderSerializer(all_orders_page, many=True)
            all_orders_data = OrderSerializer(all_orders, many=True).data
            return paginator.get_paginated_response(all_orders_data)
        else:
            raise PermissionDenied("This request is only available to Admin.")

    def post(self, request, table_id=None):
        """Creates a new order and returns the created order as a JSON."""
        data = request.data.copy()
        if table_id is not None:
            if "bill" in request.data:
                raise PermissionDenied(
                    "You are not allowed to request to add to another bill."
                )
            table = get_object_or_404(Table, pk=table_id)
            bill = table.bills.filter(active=True).first()
            if bill is None:
                raise Http404("No active bill for this table. Contact staff.")
            data["bill"] = bill.pk

        elif not (request.user.is_staff and request.user.is_superuser):
            raise PermissionDenied("This request is only available to Admin.")

        serializer = OrderSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def patch(self, request, order_id, table_id=None):
        """Edits an existing order and returns the edited version."""
        order = self.get_order_based_on_permissions(request, order_id, table_id)
        update_order = OrderPatchSerializer(order, data=request.data, partial=True)
        update_order.is_valid(raise_exception=True)
        if update_order.validated_data.get("quantity") == 0:
            return self.delete(request, order_id)
        update_order.save()
        return Response(update_order.data)

    def delete(self, request, order_id, table_id):
        """Deletes the mentioned order."""
        order = self.get_order_based_on_permissions(request, order_id, table_id)
        order.delete()
        return Response(status=status.HTTP_204)
