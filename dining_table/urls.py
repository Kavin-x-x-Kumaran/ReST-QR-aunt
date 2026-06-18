"""
URL configuration for dining_table app.
"""

from django.urls import path, include

from .routers import table_router
from .views import BillView

urlpatterns = [
    path("", include(table_router.urls)),                                       # For tables/: all: PUT, PATCH; admin: GET, POST, DELETE  
    path("tables/<int:table_id>/bills/", BillView.as_view()),                   # all: GET(active), PATCH, POST; Admin: GET(all with table_id)
    path("tables/<int:table_id>/bills/<int:bill_id>", BillView.as_view()),      # Admin: Get with bill_id
    path("bills/", BillView.as_view()),                                         # Admin: GET(all)
    path("bills/<int:bill_id>/", BillView.as_view()),                           # Admin: GET, PATCH, DELETE
]
