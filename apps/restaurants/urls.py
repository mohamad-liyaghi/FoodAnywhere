from django.urls import path, include
from restaurants.views.vendor import RestaurantListCreateView, RestaurantView
from restaurants.views.customer import NearbyRestaurantListView

app_name = "restaurants"

VENDOR_URLS = [
    path("", RestaurantListCreateView.as_view(), name="vendor-list-create"),
    path("<uuid:uuid>/", RestaurantView.as_view(), name="vendor-detail"),
]
CUSTOMER_URLS = [
    path("", NearbyRestaurantListView.as_view(), name="nearby"),
]

urlpatterns = [
    path("vendor/", include(VENDOR_URLS)),
    path("customer/", include(CUSTOMER_URLS)),
]
