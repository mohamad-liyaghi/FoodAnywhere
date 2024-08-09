from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
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
    post=extend_schema(
        summary="Create a product for a restaurant",
        description="Create a product for a restaurant",
        responses={
            201: ProductSerializer,
            400: OpenApiResponse(description="Bad request"),
            403: OpenApiResponse(description="Authentication credentials were not provided"),
            404: OpenApiResponse(description="Restaurant not found"),
        },
        tags=["Products"],
    ),
)
class ProductListCreateView(ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        restaurant = self._get_restaurant()
        return Product.objects.select_related("restaurant", "restaurant__owner").filter(
            restaurant=restaurant, is_deleted=False
        )

    def _get_restaurant(self, for_creation=False):
        if not for_creation:
            return get_object_or_404(
                Restaurant,
                uuid=self.kwargs["restaurant_uuid"],
                status=RestaurantStatus.APPROVED,
            )

        return get_object_or_404(
            Restaurant,
            uuid=self.kwargs["restaurant_uuid"],
            status=RestaurantStatus.APPROVED,
            owner=self.request.user,
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["restaurant"] = self._get_restaurant(for_creation=True)
        context["request"] = self.request
        return context


@extend_schema_view(
    get=extend_schema(
        summary="Get a product",
        description="Retrieve a product",
        responses={
            200: ProductSerializer,
            403: OpenApiResponse(description="Authentication credentials were not provided"),
            404: OpenApiResponse(description="Not found"),
        },
        tags=["Products"],
    ),
    put=extend_schema(
        summary="Update a product by its owner",
        description="Update a product",
        responses={
            200: ProductSerializer,
            400: OpenApiResponse(description="Bad request"),
            403: OpenApiResponse(description="Authentication credentials were not provided"),
            404: OpenApiResponse(description="Not found"),
        },
        tags=["Products"],
    ),
    patch=extend_schema(
        summary="Update a product by its owner",
        description="Update a product",
        responses={
            200: ProductSerializer,
            400: OpenApiResponse(description="Bad request"),
            403: OpenApiResponse(description="Authentication credentials were not provided"),
            404: OpenApiResponse(description="Not found"),
        },
        tags=["Products"],
    ),
    delete=extend_schema(
        summary="Delete a product by its owner",
        description="Delete a product",
        responses={
            204: OpenApiResponse(description="No content"),
            403: OpenApiResponse(description="Authentication credentials were not provided"),
            404: OpenApiResponse(description="Not found"),
        },
        tags=["Products"],
    ),
)
class ProductDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        if self.request.method == "GET":
            return get_object_or_404(
                Product.objects.select_related("restaurant"),
                uuid=self.kwargs["product_uuid"],
                restaurant__uuid=self.kwargs["restaurant_uuid"],
                is_deleted=False,
            )
        return get_object_or_404(
            Product.objects.select_related("restaurant"),
            uuid=self.kwargs["product_uuid"],
            restaurant__uuid=self.kwargs["restaurant_uuid"],
            restaurant__owner=self.request.user,
            is_deleted=False,
        )

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
