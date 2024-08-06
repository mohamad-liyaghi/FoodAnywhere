from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema_view, OpenApiResponse, extend_schema
from products.models import Product
from carts.services import CartService
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

    def get_object(self, product_id):
        return get_object_or_404(Product, id=product_id, is_deleted=False)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            response = CartService.add_item(
                product=self.get_object(serializer.validated_data["product_id"]),
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
