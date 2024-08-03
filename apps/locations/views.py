from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema_view, OpenApiResponse, extend_schema
from locations.models import Location
from locations.serializers import LocationSerializer


@extend_schema_view(
    get=extend_schema(
        summary="Get Locations",
        description="Get locations for the logged in user.",
        responses={
            200: LocationSerializer(many=True),
            403: OpenApiResponse(description="Unauthorized"),
        },
        tags=["Locations"],
    ),
)
class LocationListCreateView(ListAPIView):
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Location.objects.select_related("user").filter(user=self.request.user)
