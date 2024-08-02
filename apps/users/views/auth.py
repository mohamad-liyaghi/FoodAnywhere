from rest_framework.generics import CreateAPIView
from drf_spectacular.utils import extend_schema_view, OpenApiResponse, extend_schema
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import AccessToken
from users.serializers import (
    AccessTokenObtainSerializer,
    AccessTokenRefreshSerializer,
)
from users.models import User
from users.serializers import UserRegisterSerializer
from active_sessions.models import ActiveSession
from active_sessions.enums import LoginDeviceType, LoginBrowserType


@extend_schema_view(
    post=extend_schema(
        summary="Register a new user",
        description="Create a new user in database",
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
        request=AccessTokenObtainSerializer,
        responses={
            200: OpenApiResponse(description="Access token retrieved"),
            400: OpenApiResponse(description="Invalid Data"),
            401: OpenApiResponse(description="Invalid email/password"),
        },
        tags=["Authentication"],
    ),
)
class AccessTokenObtainView(TokenObtainPairView):
    serializer_class = AccessTokenObtainSerializer

    def post(self, request, *args, **kwargs):
        token = super().post(request, *args, **kwargs)
        user = User.objects.get(email=request.data["email"])
        ActiveSession.objects.create(
            user=user,
            device_type=request.data.get("device_type", LoginDeviceType.UNKNOWN),
            browser_type=request.data.get("browser_type", LoginBrowserType.UNKNOWN),
            ip_address=request.META.get("REMOTE_ADDR"),
        )
        return token


@extend_schema_view(
    post=extend_schema(
        summary="Refresh access token",
        description="""Refresh access token for the user.""",
        request=AccessTokenRefreshSerializer,
        responses={
            200: OpenApiResponse(description="Access token refreshed"),
            400: OpenApiResponse(description="Invalid Data"),
            401: OpenApiResponse(description="Invalid token"),
        },
        tags=["Authentication"],
    ),
)
class AccessTokenRefreshView(TokenRefreshView):
    serializer_class = AccessTokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        access_token = super().post(request, *args, **kwargs)
        token = AccessToken(access_token.data["access"])
        user_id = token.payload["user_id"]
        user = User.objects.get(id=user_id, is_active=True)
        ActiveSession.objects.create(
            user=user,
            device_type=request.data.get("device_type", LoginDeviceType.UNKNOWN),
            browser_type=request.data.get("browser_type", LoginBrowserType.UNKNOWN),
            ip_address=request.META.get("REMOTE_ADDR"),
        )
        return access_token
