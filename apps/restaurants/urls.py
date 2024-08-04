from django.urls import path, include
from restaurants.views.vendor import (
    RestaurantListCreateView,
    RestaurantView,
)

app_name = "restaurants"

VENDOR_URLS = [
    path("", RestaurantListCreateView.as_view(), name="vendor-list-create"),
    path("<uuid:uuid>/", RestaurantView.as_view(), name="vendor-detail"),
]
CUSTOMER_URLS = []

urlpatterns = [
    path("vendor/", include(VENDOR_URLS)),
    path("customer/", include(CUSTOMER_URLS)),
]
