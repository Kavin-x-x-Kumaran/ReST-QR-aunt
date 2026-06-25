"""
Views for dining tables, and bills.

Provides views for accommodating HTTP requests.
"""

from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Bill, Table
from .permissions import IsAllowedAccess
from .serializers import BillSerializer, TableSerializer


class TableView(ModelViewSet):
    """
    Viewset for managing tables.

    Restricts access to based on IsAllowedAccess permission class.
    """

    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = [IsAllowedAccess]


class BillView(APIView):
    """
    View for accessing bills.
    """

    pagination_class = PageNumberPagination
    PAGINATION_PAGE_SIZE = 100

    def get(self, request, table_id=None, bill_id=None):
        """
        - If bill_id is present:
            > If user is not a superuser: Raises HTTP 403
            > If user is a superuser: Returns the requested bill.
        - If bill_id is absent and table_id is present:
            > If user is not a superuser: Returns the active bill of the mentioned table (if exists, else 404).
            > If user is a superuser: Returns all bills of the mentioned table in a paginated manner.
        - If both bill_id and table_id are absent:
            > If user is not a superuser: Returns HTTP 404
            > If user is a superuser: Returns all bills in a paginated manner.
        """
        paginator = self.pagination_class()
        paginator.page_size = self.PAGINATION_PAGE_SIZE
        authorised = (
            request.user
            and request.user.is_authenticated
            and request.user.is_staff
            and request.user.is_superuser
        )
        if bill_id is not None:
            if not authorised:
                raise PermissionDenied("Only admin can perform this action.")
            bill = get_object_or_404(Bill, pk=bill_id)
            bill_data = BillSerializer(bill).data
            return Response(bill_data)

        if table_id is not None:
            # If table_id is present
            table = get_object_or_404(Table, pk=table_id)

            if authorised:
                # If bill_id is absent, table_id is present and the user is a superuser.
                table_bills = table.bills.all()
                if table_bills is None:
                    raise Http404("No bills exist for this table.")
                table_bills_page = paginator.paginate_queryset(table_bills, request)
                table_bills_data = BillSerializer(table_bills_page, many=True).data
                return paginator.get_paginated_response(table_bills_data)

            # If bill_id is present, table_id is absent and user is not a superuser.
            bill = table.bills.filter(active=True).first()
            bill_data = BillSerializer(bill).data
            if bill is None:
                raise Http404("No active bill exists for this table. Contact staff.")
            bill_data = BillSerializer(bill).data
            return Response(bill_data)

        if not authorised:
            raise Http404("Table_id not found.")

        all_bills = Bill.objects.all()
        result_page = paginator.paginate_queryset(all_bills, request)
        all_bills_data = BillSerializer(result_page, many=True).data
        return paginator.get_paginated_response(all_bills_data)

    def post(self, request, table_id):
        """
        Function to create new bills.
        """
        table = get_object_or_404(Table, pk=table_id)
        if table.bills.filter(active=True).exists():
            raise ValidationError(
                "No bill created. There already exists a bill at this table. Contact staff."
            )

        new_bill = Bill(table=table, active=True)
        new_bill.save()
        new_bill_data = BillSerializer(new_bill).data
        return Response(new_bill_data, status=status.HTTP_201_CREATED)

    def patch(self, request, table_id=None, bill_id=None):
        """
        Updates the active bill of the given table/bill_id and returns updated bill data.
        """
        if bill_id is not None:
            if not (request.user.is_staff and request.user.is_superuser):
                raise PermissionDenied("Only admin can perform this action.")
            bill = get_object_or_404(Bill, pk=bill_id)

        elif table_id is not None:
            table = get_object_or_404(Table, pk=table_id)
            bill = table.bills.filter(active=True).first()
            if bill is None:
                raise Http404("No active bill at the given table.")

        else:
            raise Http404("Table_id and bill_id not found.")

        update_bill = BillSerializer(bill, data=request.data, partial=True)
        update_bill.is_valid(raise_exception=True)
        update_bill.save()
        return Response(update_bill.data)

    def delete(self, request, bill_id):
        """
        Deletes the mentioned bill_id.
        """
        authorised = (
            request.user
            and request.user.is_authenticated
            and request.user.is_staff
            and request.user.is_superuser
        )
        if authorised:
            bill = get_object_or_404(Bill, pk=bill_id)
            bill.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise PermissionDenied("Only admin can perform this action.")
