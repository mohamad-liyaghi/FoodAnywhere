from django.urls import path, include
from restaurants.views.vendor import VendorRestaurantListCreateView

app_name = "restaurants"

VENDOR_URLS = [
    path("", VendorRestaurantListCreateView.as_view(), name="vendor-list-create"),
]
CUSTOMER_URLS = []

urlpatterns = [
    path("vendor/", include(VENDOR_URLS)),
    path("customer/", include(CUSTOMER_URLS)),
]
