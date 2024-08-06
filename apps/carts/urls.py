from django.urls import path
from carts.views import CartListCreateView, CartDestroyView

app_name = "carts"

urlpatterns = [
    path("", CartListCreateView.as_view(), name="list-create"),
    path("<uuid:product_uuid>/", CartDestroyView.as_view(), name="delete"),
]
