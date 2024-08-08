from django.urls import path, include
from orders.views.customer import OrderListCreateView, OrderPayView, OrderCancelView
from orders.views.vendor import VendorOrderListView

app_name = "orders"

VENDOR_URLS = [
    path("", VendorOrderListView.as_view(), name="vendor-list"),
]
CUSTOMER_URLS = [
    path("", OrderListCreateView.as_view(), name="customer-list-create"),
    path("<uuid:uuid>/pay/", OrderPayView.as_view(), name="customer-pay"),
    path("<uuid:uuid>/cancel/", OrderCancelView.as_view(), name="customer-cancel"),
]

urlpatterns = [
    path("vendor/", include(VENDOR_URLS)),
    path("customer/", include(CUSTOMER_URLS)),
]
