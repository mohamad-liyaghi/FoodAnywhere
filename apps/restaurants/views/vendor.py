from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from drf_spectacular.utils import extend_schema_view, OpenApiResponse, extend_schema
from rest_framework.permissions import IsAuthenticated
from restaurants.models import Restaurant
from restaurants.enums import RestaurantStatus
from restaurants.serializers import RestaurantSerializer


@extend_schema_view(
    get=extend_schema(
        summary="List of vendors restaurants",
        description="Get all restaurants that a user owns.",
        responses={
            200: RestaurantSerializer(many=True),
            403: OpenApiResponse(description="Unauthorized"),
        },
        tags=["Vendor Restaurants"],
    ),
    post=extend_schema(
        summary="Create a restaurant",
        description="Create a new restaurant.",
        request=RestaurantSerializer,
        responses={
            201: RestaurantSerializer,
            400: OpenApiResponse(description="Bad request"),
            403: OpenApiResponse(description="Unauthorized"),
        },
        tags=["Vendor Restaurants"],
    ),
)
class VendorRestaurantListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RestaurantSerializer

    def get_queryset(self):
        return Restaurant.objects.select_related("owner").filter(owner=self.request.user, is_soft_deleted=False)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user, status=RestaurantStatus.REQUESTED)


@extend_schema_view(
    get=extend_schema(
        summary="Get a restaurant",
        description="Get a restaurant by id.",
        responses={
            200: RestaurantSerializer,
            403: OpenApiResponse(description="Unauthorized"),
            404: OpenApiResponse(description="Not found"),
        },
        tags=["Vendor Restaurants"],
    ),
    put=extend_schema(
        summary="Update a restaurant",
        description="Update a restaurant by id.",
        request=RestaurantSerializer,
        responses={
            200: RestaurantSerializer,
            400: OpenApiResponse(description="Bad request"),
            403: OpenApiResponse(description="Unauthorized"),
            404: OpenApiResponse(description="Not found"),
        },
        tags=["Vendor Restaurants"],
    ),
    delete=extend_schema(
        summary="Delete a restaurant",
        description="Delete a restaurant by id.",
        responses={
            204: OpenApiResponse(description="No content"),
            403: OpenApiResponse(description="Unauthorized"),
            404: OpenApiResponse(description="Not found"),
        },
        tags=["Vendor Restaurants"],
    ),
)
class VendorRestaurantView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RestaurantSerializer

    def get_object(self):
        if self.request.method == "GET":
            return get_object_or_404(
                Restaurant.objects.select_related("owner"),
                uuid=self.kwargs["uuid"],
                status=RestaurantStatus.APPROVED,
                is_soft_deleted=False,
            )
        return get_object_or_404(
            Restaurant.objects.select_related("owner"),
            uuid=self.kwargs["uuid"],
            owner=self.request.user,
            status__in=[RestaurantStatus.REQUESTED, RestaurantStatus.APPROVED],
            is_soft_deleted=False,
        )

    def perform_destroy(self, instance):
        instance.is_soft_deleted = True
        instance.save()
