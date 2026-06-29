"""
URL configuration for dining_table app.
"""

from rest_framework_nested import routers
from rest_framework.routers import DefaultRouter

from order.views import OrderViewSet, OrderTableViewSet
from .views import BillAdminViewSet, BillTableViewSet, TableViewSet

urlpatterns = []

router = DefaultRouter()
router.register(r"tables", TableViewSet)
router.register(r"bills", BillAdminViewSet)
urlpatterns += router.urls

table_nested_router = routers.NestedDefaultRouter(router, "tables", lookup="table")
table_nested_router.register(r"bills", BillTableViewSet, basename="table-bills")
table_nested_router.register(
    r"orders", OrderTableViewSet, basename="table-current-orders"
)
urlpatterns += table_nested_router.urls

bill_nested_router = routers.NestedDefaultRouter(router, "bills", lookup="bill")
bill_nested_router.register(r"orders", OrderViewSet, basename="bill-orders")
urlpatterns += bill_nested_router.urls
