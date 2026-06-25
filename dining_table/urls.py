"""
URL configuration for dining_table app.
"""

from rest_framework_nested import routers
from rest_framework.routers import DefaultRouter

from .views import BillAdminViewSet, BillTableViewSet, TableViewSet

urlpatterns = []

router = DefaultRouter()
router.register(r'tables', TableViewSet)
router.register(r'bills', BillAdminViewSet)
urlpatterns += router.urls

table_bill_router = routers.NestedDefaultRouter(router, "tables", lookup="table")
table_bill_router.register(r'bills', BillTableViewSet, basename="table-bills")
urlpatterns += table_bill_router.urls
