from django.urls import path, include
from orders.views.customer import (
    OrderListCreateView,
    OrderPayView,
    OrderCancelView,
    OrderDeliveredView,
)
from orders.views.vendor import VendorOrderListView, VendorOrderSetShippedView

app_name = "orders"

VENDOR_URLS = [
    path("", VendorOrderListView.as_view(), name="vendor-list"),
    path(
        "<uuid:uuid>/shipped/",
        VendorOrderSetShippedView.as_view(),
        name="vendor-shipped",
    ),
]
CUSTOMER_URLS = [
    path("", OrderListCreateView.as_view(), name="customer-list-create"),
    path("<uuid:uuid>/pay/", OrderPayView.as_view(), name="customer-pay"),
    path("<uuid:uuid>/cancel/", OrderCancelView.as_view(), name="customer-cancel"),
    path(
        "<uuid:uuid>/delivered/",
        OrderDeliveredView.as_view(),
        name="customer-delivered",
    ),
]

urlpatterns = [
    path("vendor/", include(VENDOR_URLS)),
    path("customer/", include(CUSTOMER_URLS)),
]
