from django.urls import path, include
from orders.views.customer import OrderListCreateView

app_name = "orders"

VENDOR_URLS = []
CUSTOMER_URLS = [
    path("", OrderListCreateView.as_view(), name="customer-list-create"),
]

urlpatterns = [
    path("vendor/", include(VENDOR_URLS)),
    path("customer/", include(CUSTOMER_URLS)),
]
