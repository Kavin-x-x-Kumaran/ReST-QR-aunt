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
    #pagination_class = PageNumberPagination

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

        - Raises HTTP 404 if an invalid order_id is passed as argument.
        - Returns the requested order if a valid order_id is passed as argument.
        - Raises HTTP 404 if an invalid table_id is passed as argument.
        - Returns all the orders of the active bill of the passed table.
        - Raises HTTP 404 if an invalid bill_id is passed as argument.
        - Returns all orders of the mentioned bill corresponding to the passed valid bill_id.
        - Raises HTTP 403 if a non-staff member attempts to access orders filtered by status.
        - Raises HTTP 404 if an invalid status is passed as argument.
        - Returns all orders of the mentioned valid status passed as argument when request is made by a member of staff.
        - Raises HTTP 403 if a non-superuser attempts to access all orders.
        - Returns all orders, If no arguments are passed if request is made by a superuser.
        """
        if order_id is not None:
            order = get_object_or_404(Order, pk=order_id)
            order_data = OrderSerializer(order).data
            return Response(order_data)

        if table_id is not None:
            table = get_object_or_404(Table, pk=table_id)
            bill = table.bills.filter(active=True).first()
            if bill is None:
                raise Http404("No active bill exists for this table.")
            bill_id = bill.id

        if bill_id is not None:
            bill = get_object_or_404(Bill, pk=bill_id)
            orders = bill.orders.all()
            orders_data = OrderSerializer(orders, many=True).data
            return Response(orders_data)

        if status is not None:
            if not request.user.is_staff:
                raise PermissionDenied("This request is only available to staff.")
            if status.upper() not in ["O", "W", "D"]:
                raise Http404("Invalid status entered.")
            status_orders = Order.objects.filter(status=status.upper())
            if not status_orders.exists():
                return Response("No orders left of this status.")
            status_orders_data = OrderSerializer(status_orders, many=True).data
            return Response(status_orders_data)

        if request.user.is_staff and request.user.is_superuser:
            all_orders = Order.objects.all()
            all_orders_data = OrderSerializer(all_orders, many=True).data
            return Response(all_orders_data)
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
