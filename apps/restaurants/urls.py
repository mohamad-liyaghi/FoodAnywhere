from django.urls import path, include

app_name = "restaurants"

VENDOR_URLS = []
CUSTOMER_URLS = []

urlpatterns = [
    path("vendor/", include(VENDOR_URLS)),
    path("customer/", include(CUSTOMER_URLS)),
]
