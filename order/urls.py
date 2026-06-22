"""
URL configuration for order app.
"""

from django.urls import path

from .views import OrderView

urlpatterns = [
    path("bills/<int:bill_id>/orders/<int:order_id>/", OrderView.as_view()),        # Admin only: GET, POST, DELETE
    path("bills/<int:bill_id>/orders/", OrderView.as_view()),                       # Admin only: GET(all), POST
    path("kitchen/orders/<str:status>", OrderView.as_view()),                       # Staff: PATCH
    path("tables/<int:table_id>/orders/<int:order_id>/", OrderView.as_view()),      # Customers: PATCH, DELETE
    path("tables/<int:table_id>/orders/", OrderView.as_view()),                     # Customers: GET(all), POST
    path("orders/status/<str:status>/", OrderView.as_view()),                       # Admin only: GET
    path("orders/<int:order_id>", OrderView.as_view()),                             # Admin only: GET, PATCH, DELETE
    path("orders/", OrderView.as_view()),                                           # Admin only: GET(all), POST
]