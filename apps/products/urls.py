from django.urls import path
from products.views import ProductListCreateView

app_name = "products"

urlpatterns = [
    path(
        "<uuid:restaurant_uuid>/",
        ProductListCreateView.as_view(),
        name="list-create",
    ),
]
