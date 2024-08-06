from django.urls import path
from carts.views import CartListCreateView, CartUpdateDestroyView

app_name = "carts"

urlpatterns = [
    path("", CartListCreateView.as_view(), name="list-create"),
    path("<uuid:product_uuid>/", CartUpdateDestroyView.as_view(), name="update-delete"),
]
