from django.urls import path, include
from orders.views.customer import OrderListCreateView, OrderPayView, OrderCancelView

app_name = "orders"

VENDOR_URLS = []
CUSTOMER_URLS = [
    path("", OrderListCreateView.as_view(), name="customer-list-create"),
    path("<uuid:uuid>/pay/", OrderPayView.as_view(), name="customer-pay"),
    path("<uuid:uuid>/cancel/", OrderCancelView.as_view(), name="customer-cancel"),
]

urlpatterns = [
    path("vendor/", include(VENDOR_URLS)),
    path("customer/", include(CUSTOMER_URLS)),
]
