"""
URL configuration for dining_table app.
"""

from django.urls import path, include

from .views import BillView, TableView

urlpatterns = [
    path(
        "tables/<int:pk>/",                                                     # all: PATCH; admin: GET, DELETE
        TableView.as_view(
            actions=({"get": "retrieve", "patch": "update", "delete": "destroy"})
        ),
    ),
    path(                                                                       # admin: GET, POST
        "tables/", TableView.as_view(actions=({"get":"list", "post":"create"}))
    ),
    path("tables/<int:table_id>/bills/", BillView.as_view()),                   # all: GET(active), PATCH, POST; Admin: GET(all with table_id)
    path("tables/<int:table_id>/bills/<int:bill_id>", BillView.as_view()),      # Admin: Get with bill_id
    path("bills/", BillView.as_view()),                                         # Admin: GET(all)
    path("bills/<int:bill_id>/", BillView.as_view()),                           # Admin: GET, PATCH, DELETE
]
