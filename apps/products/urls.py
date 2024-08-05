from django.urls import path
from products.views import ProductListCreateView, ProductDetailView

app_name = "products"

urlpatterns = [
    path(
        "<uuid:restaurant_uuid>/",
        ProductListCreateView.as_view(),
        name="list-create",
    ),
    path(
        "<uuid:restaurant_uuid>/<uuid:product_uuid>/",
        ProductDetailView.as_view(),
        name="detail",
    ),
]
