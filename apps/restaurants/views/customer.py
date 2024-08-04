from django.contrib.gis.db.models.functions import Distance
from rest_framework.generics import ListAPIView
from drf_spectacular.utils import extend_schema_view, OpenApiResponse, extend_schema
from rest_framework.permissions import IsAuthenticated
from restaurants.models import Restaurant
from restaurants.enums import RestaurantStatus
from restaurants.serializers import RestaurantSerializer


@extend_schema_view(
    get=extend_schema(
        summary="List of nearby restaurants",
        description="Get all nearby restaurants.",
        responses={
            200: RestaurantSerializer(many=True),
            403: OpenApiResponse(description="Unauthorized"),
        },
        tags=["Customer Restaurants"],
    )
)
class NearbyRestaurantListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RestaurantSerializer

    def get_queryset(self):
        user_primary_location = self.request.user.locations.filter(is_primary=True).first()
        return (
            Restaurant.objects.annotate(distance=Distance("location", user_primary_location.location))
            .order_by("distance")
            .filter(is_soft_deleted=False, status=RestaurantStatus.APPROVED)
        )
