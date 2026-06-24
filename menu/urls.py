"""
URL configuration for menu app.
"""

from django.urls import path

from .views import (
    CategoryAdminView,
    CategoryListView,
    ItemAdminView,
    ItemListView,
    ItemStaffView,
)

urlpatterns = [
    path("categories/", CategoryListView.as_view()),                        # all: GET(all)
    path("categories/<int:pk>/", CategoryListView.as_view()),               # all: GET
    path("items/", ItemListView.as_view()),                                 # all: GET(all)
    path("items/<int:pk>/", ItemListView.as_view()),                        # all: GET
    path("kitchen/items/<int:pk>/", ItemStaffView.as_view()),               # Staff and Admin: PATCH (only Availability)
    path("admin/categories/", CategoryAdminView.as_view(                    # Admin only: GET(all), POST
        {'get':'list', 'post':'create'}
    )),
    path("admin/categories/<int:pk>/", CategoryAdminView.as_view(           # Admin only: GET, PATCH, PUT,        
        {'get':'retrieve', 'patch':'update', 'put':'update'}
    )),
    path("admin/items/", ItemAdminView.as_view(                             # Admin only: GET(all), POST
        {'get':'list', 'post':'create'}
    )),
    path("admin/items/<int:pk>/", ItemAdminView.as_view(                    # Admin only: GET, PATCH, PUT,        
        {'get':'retrieve', 'patch':'update', 'put':'update'}
    )),
]
