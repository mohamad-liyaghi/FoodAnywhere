from django.urls import path, include
from orders.views.customer import OrderListCreateView, OrderPayView

app_name = "orders"

VENDOR_URLS = []
CUSTOMER_URLS = [
    path("", OrderListCreateView.as_view(), name="customer-list-create"),
    path("<uuid:uuid>/pay/", OrderPayView.as_view(), name="customer-pay"),
]

urlpatterns = [
    path("vendor/", include(VENDOR_URLS)),
    path("customer/", include(CUSTOMER_URLS)),
]
