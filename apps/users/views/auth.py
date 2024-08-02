from rest_framework.generics import CreateAPIView
from drf_spectacular.utils import extend_schema_view, OpenApiResponse, extend_schema
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
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


@extend_schema_view(
    post=extend_schema(
        summary="Get access token",
        description="""Get access token for the user.""",
        request=TokenObtainPairSerializer,
        responses={
            200: OpenApiResponse(description="Access token retrieved"),
            400: OpenApiResponse(description="Invalid Data"),
            401: OpenApiResponse(description="Invalid email/password"),
        },
        tags=["Authentication"],
    ),
)
class AccessTokenObtainView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer
