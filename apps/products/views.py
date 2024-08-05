from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema_view, OpenApiResponse, extend_schema
from products.models import Product
from restaurants.models import Restaurant
from restaurants.enums import RestaurantStatus
from products.serializers import ProductSerializer


@extend_schema_view(
    get=extend_schema(
        summary="Get all products for a restaurant",
        description="Retrieve all products for a restaurant",
        responses={
            200: ProductSerializer(many=True),
            403: OpenApiResponse(description="Authentication credentials were not provided"),
            404: OpenApiResponse(description="Not found"),
        },
        tags=["Products"],
    ),
)
class ProductListCreateView(ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        restaurant = get_object_or_404(
            Restaurant,
            uuid=self.kwargs["restaurant_uuid"],
            status=RestaurantStatus.APPROVED,
        )
        return Product.objects.select_related("restaurant", "restaurant__owner").filter(
            restaurant=restaurant
        )  # TODO: make this single query
