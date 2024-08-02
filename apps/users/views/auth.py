from rest_framework.generics import CreateAPIView
from drf_spectacular.utils import extend_schema_view, OpenApiResponse, extend_schema
from users.serializers import UserRegisterSerializer


@extend_schema_view(
    post=extend_schema(
        summary="Register a new user",
        description="Create a new user in databasse",
        responses={
            201: UserRegisterSerializer(),
            400: OpenApiResponse(description="Bad Request"),
        },
        tags=["Authentication"],
    ),
)
class UserRegisterView(CreateAPIView):
    serializer_class = UserRegisterSerializer
