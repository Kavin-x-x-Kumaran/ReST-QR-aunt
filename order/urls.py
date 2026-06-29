"""
URL configuration for order app.
"""

from rest_framework.routers import DefaultRouter

from .views import OrderViewSet

# from django.urls import path

# from .views import OrderView

urlpatterns = [
    # path("bills/<int:bill_id>/orders/<int:order_id>/", OrderView.as_view()),        # Staff: GET, POST, DELETE
    # path("bills/<int:bill_id>/orders/", OrderView.as_view()),                       # Staff: GET(all), POST
    # path("tables/<int:table_id>/orders/<int:order_id>/", OrderView.as_view()),      # Customers: PATCH, DELETE
    # path("tables/<int:table_id>/orders/", OrderView.as_view()),                     # Customers: GET(all), POST
    # path("orders/status/<str:status>/", OrderView.as_view()),                       # Staff: GET
    # path("orders/<int:order_id>/", OrderView.as_view()),                            # Staff: GET, PATCH, DELETE
    # path("orders/", OrderView.as_view()),                                           # Staff: GET(all), POST
]

router = DefaultRouter()
router.register(r"orders", OrderViewSet)
urlpatterns += router.urls
