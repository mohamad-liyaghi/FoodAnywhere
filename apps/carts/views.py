from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema_view, OpenApiResponse, extend_schema
from carts.services import CartService
from products.models import Product
from carts.exceptions import MaximumQuantityExceeded
from carts.serializers import CartSerializer


@extend_schema_view(
    post=extend_schema(
        summary="Add product to cart",
        description="Add product to cart",
        request=CartSerializer,
        responses={
            201: OpenApiResponse(description="Product added to cart"),
            400: OpenApiResponse(description="Bad Request or Maximum quantity exceeded"),
            403: OpenApiResponse(description="Authentication credentials were not provided"),
        },
        tags=["Cart"],
    ),
    get=extend_schema(
        summary="Get cart items",
        description="Get cart items",
        responses={
            200: OpenApiResponse(description="Cart items"),
            403: OpenApiResponse(description="Authentication credentials were not provided"),
        },
        tags=["Cart"],
    ),
)
class CartListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    def get_queryset(self):
        return CartService.get_items(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            response = CartService.add_item(
                product=serializer.validated_data["product"],
                quantity=serializer.validated_data["quantity"],
                user=request.user,
            )
        except MaximumQuantityExceeded:
            return Response(
                {"error": "Maximum quantity exceeded"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(response, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        response = self.get_queryset()
        return Response(response, status=status.HTTP_200_OK)


@extend_schema_view(
    delete=extend_schema(
        summary="Remove product from cart",
        description="Remove product from cart",
        responses={
            204: OpenApiResponse(description="Product removed from cart"),
            403: OpenApiResponse(description="Authentication credentials were not provided"),
            404: OpenApiResponse(description="Not found"),
        },
        tags=["Cart"],
    ),
)
class CartDestroyView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    def get_object(self):
        product = get_object_or_404(Product, uuid=self.kwargs["product_uuid"], is_deleted=False)
        return product

    def perform_destroy(self, instance):
        CartService.remove_item(user=self.request.user, product=instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
