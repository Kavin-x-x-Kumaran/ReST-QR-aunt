"""
Views for dining tables, and bills.

Provides views for accommodating HTTP requests.
"""

from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import PermissionDenied, ValidationError
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

    def get(self, request, table_id=None, bill_id=None):
        """
        - If bill_id is present:
            > If user is not a superuser: Raises HTTP 403
            > If user is a superuser: Returns the requested bill.
        - If bill_id is absent and table_id is present:
            > If user is not a superuser: Returns the active bill of the mentioned table (if exists, else 404).
            > If user is a superuser: Returns all bills of the mentioned table.
        - If both bill_id and table_id are absent:
            > If user is not a superuser: Returns HTTP 404
            > If user is a superuser: Returns all bills.
        """
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

            if (
                authorised
            ):  # If bill_id is absent, table_id is present and the user is a superuser.
                table_bills = table.bills.all()
                if table_bills is None:
                    raise Http404("No bills exist for this table.")
                table_bills_data = BillSerializer(table_bills, many=True).data
                return Response(table_bills_data)

            # If bill_id is present, table_id is absent and user is not a superuser.
            bill_data = BillSerializer(bill).data
            bill = table.bills.filter(active=True).first()
            if bill is None:
                raise Http404("No active bill exists for this table. Contact staff.")
            bill_data = BillSerializer(bill).data
            return Response(bill_data)
        
        if not authorised:
            raise Http404("Table_id not found.")
        
        all_bills = Bill.objects.all()
        all_bills_data = BillSerializer(all_bills, many=True).data
        return Response(all_bills_data)

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
            return Response(status=status.HTTP_204)
        else:
            raise PermissionDenied("Only admin can perform this action.")
