"""
Views for dining tables, and bills.

Provides views for accommodating HTTP requests.
"""

from rest_framework import status
from rest_framework.exceptions import ParseError, PermissionDenied, ValidationError
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from REST_QR_aunt.pagination import DefaultPageNumberPagination
from REST_QR_aunt.permissions import IsSuperUser
from .models import Bill, Table
from .permissions import IsAllowedAccess
from .serializers import BillSerializer, TableSerializer


class TableViewSet(ModelViewSet):
    """
    Viewset for managing tables.

    Restricts access to based on IsAllowedAccess permission class.
    """

    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = [IsAllowedAccess]
    lookup_field = "public_id"


class BillAdminViewSet(ModelViewSet):
    """
    Viewset for managing bills.

    Restricts access to superusers.
    """

    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    permssion_classes = [IsSuperUser]
    pagination_class = DefaultPageNumberPagination
    lookup_field = "public_id"

    def create(self, request, *args, **kwargs):
        """
        Create a Bill instance.
        """
        table = request.data.get("table")
        if table is None:
            raise ParseError("'tabe' field required.")
        if table.bills.filter(active=True).exists():
            raise ValidationError(
                "No bill created. There already exists a bill at this table. Contact staff."
            )
        new_bill = Bill(table=table, active=request.data("active", True))
        new_bill.save()
        new_bill_data = self.get_serializer(new_bill).data
        return Response(new_bill_data, status=status.HTTP_201_CREATED)


class BillTableViewSet(
    GenericViewSet, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
):
    """
    Viewset for accessing bills associated with a table.

    Gives heightened access to superusers.
    """

    serializer_class = BillSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = DefaultPageNumberPagination

    def get_table(self):
        return get_object_or_404(Table, public_id=self.kwargs["table_pk"])

    def create(self, request, *args, **kwargs):
        """
        Create a Bill instance.

        If user is not a superuser (is a customer) they can only create a bill for their own table.
        """
        table = self.get_table()
        if table.bills.filter(active=True).exists():
            raise ValidationError(
                "No bill created. There already exists a bill at this table. Contact staff."
            )
        if not request.user.is_superuser:
            if table != self.request.user.table:
                raise PermissionDenied(
                    "You cannot create a bill for someone else's table."
                )
        new_bill = Bill(table=table, active=True)
        new_bill.save()
        new_bill_data = self.get_serializer(new_bill).data
        return Response(new_bill_data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        """
        Returns queryset containing the bills associated with the required table.

        If the user is not a superuser (is a customer), it returns only the active
        bills, after validating whether they are requesting their own table's bill.
        """
        table = self.get_table()
        if self.request.user.is_superuser:
            return table.bills.all()
        if table == self.request.user.table:
            return table.bills.filter(active=True)
        raise PermissionDenied("You cannot view someone else's bill.")

    def update(self, request, *args, **kwargs):
        """Returns ModelViewSet.update() if user is a superuser and raises HTTP 403 otherwise."""
        if request.user.is_superuser:
            return super().update(request, *args, **kwargs)
        raise PermissionDenied("You cannot perform this function.")
