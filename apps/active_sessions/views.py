from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema_view, OpenApiResponse, extend_schema
from active_sessions.models import ActiveSession
from active_sessions.serializers import ActiveSessionSerializer


@extend_schema_view(
    get=extend_schema(
        summary="Get active sessions",
        description="Get active sessions for the user.",
        responses={
            200: ActiveSessionSerializer(many=True),
            403: OpenApiResponse(description="Unauthorized"),
        },
        tags=["Active Sessions"],
    ),
)
class ActiveSessionListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ActiveSessionSerializer

    def get_queryset(self):
        return ActiveSession.objects.filter(user=self.request.user)[:10]
