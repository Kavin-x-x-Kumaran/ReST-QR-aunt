"""
Views for dining tables, and bills.

Provides views for accommodating HTTP requests.
"""

from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Bill, Table
from .permissions import IsAllowedAccess
from .serializers import BillSerializer, TableSerializer


class TableView(ModelViewSet):
    """
    Viewset for managing users.

    Restricts access to superusers.
    """

    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = [IsAllowedAccess]


class BillView(APIView):
    """
    View for getting bills.
    """

    def get(self, request, table_id=None, bill_id=None):
        """
        Function to GET bills associated with the given table.
        """
        if table_id is None:
            if bill_id is None:
                raise Http404("No bill_id mentioned.")
            else:
                authorised = (
                    request.user
                    and request.user.is_authenticated
                    and request.user.is_staff
                    and request.user.is_superuser
                )
                if authorised:
                    bill = get_object_or_404(Bill, pk=bill_id)
                    bill_data = BillSerializer(bill).data
                    return Response(bill_data)
                else:
                    raise PermissionDenied("Only admin can perform this action.")
        else:
            table = get_object_or_404(Table, pk=table_id)
            bill = table.bills.filter(active=True).first()
            if bill is None:
                raise Http404("No active bill exists for this table.")
            bill_data = BillSerializer(bill).data
            return Response(bill_data)

    def post(self, request, table_id):
        """
        Function to create new bills.
        """
        table = get_object_or_404(Table, pk=table_id)
        if table.bills.filter(active=True).exists():
            raise ValidationError(
                "No bill created. There already exists a bill at this table. Contact admin."
            )

        new_bill = Bill(table=table, date=timezone.now(), active=True)
        new_bill.save()
        new_bill_data = BillSerializer(new_bill).data
        return Response(new_bill_data, status=status.HTTP_201_CREATED)

    def patch(self, request, table_id):
        """
        Function to update the active bill of the given table.
        """
        table = get_object_or_404(Table, pk=table_id)
        bill = table.bills.filter(active=True).order_by("-date").first()

        if bill is None:
            raise Http404("No active bill at the given table.")

        update_bill = BillSerializer(bill, data=request.data, partial=True)

        update_bill.is_valid(raise_exception=True)
        update_bill.save()
        return Response(update_bill.data)

    def delete(self, request, bill_id):
        authorised = (
            request.user
            and request.user.is_authenticated
            and request.user.is_staff
            and request.user.is_superuser
        )
        if authorised:
            bill = get_object_or_404(Bill, pk=bill_id)
            bill.delete()
            return Response({"detail": "Bill deleted successfully."})
        else:
            raise PermissionDenied("Only admin can perform this action.")
