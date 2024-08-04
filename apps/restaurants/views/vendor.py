from rest_framework.generics import ListCreateAPIView
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
)
class VendorRestaurantListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RestaurantSerializer

    def get_queryset(self):
        return Restaurant.objects.select_related("owner").filter(owner=self.request.user)
