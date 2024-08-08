from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema_view, OpenApiResponse, extend_schema
from restaurants.models import Restaurant
from orders.models import Order
from orders.enums import OrderStatus
from orders.serializers import OrderSerializer


@extend_schema_view(
    get=extend_schema(
        summary="List Of Customer Orders",
        description="List of all orders placed by the customer",
        responses={
            200: OrderSerializer(many=True),
            403: OpenApiResponse(description="Unauthorized"),
        },
        tags=["Vendor Orders"],
    ),
)
class VendorOrderListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer

    def get_queryset(self):
        restaurant = Restaurant.objects.filter(owner=self.request.user, is_soft_deleted=False)

        if not restaurant.exists():
            return Order.objects.none()

        return (
            Order.objects.select_related("restaurant", "user")
            .prefetch_related("items", "items__product")
            .filter(restaurant__in=restaurant, status=OrderStatus.PENDING_PAYMENT)
            .order_by("-created_at")
        )


@extend_schema_view(
    post=extend_schema(
        summary="Pay for an order",
        description="Pay for an order",
        responses={
            200: OrderSerializer(),
            400: OpenApiResponse(description="Bad Request"),
            403: OpenApiResponse(description="Unauthorized"),
        },
        tags=["Customer Orders"],
    ),
)
class VendorOrderSetShippedView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return get_object_or_404(
            Order,
            uuid=self.kwargs["uuid"],
            restaurant__owner=self.request.user,
            status=OrderStatus.PROCESSING,
        )

    def post(self, request, *args, **kwargs):
        order = self.get_object()

        order.status = OrderStatus.SHIPPED
        order.save()
        return Response({"message": "Order has been shipped"}, status=status.HTTP_200_OK)
