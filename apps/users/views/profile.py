from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema_view, OpenApiResponse, extend_schema
from users.models import User
from users.serializers import UserProfileSerializer


@extend_schema_view(
    retrieve=extend_schema(
        summary="Retrieve user profile",
        description="Retrieve user profile information",
        responses={
            200: UserProfileSerializer(),
            403: OpenApiResponse(description="Authentication credentials were not provided"),
        },
        tags=["Profile"],
    ),
    update=extend_schema(
        summary="Update user profile",
        description="Update user profile information",
        responses={
            200: UserProfileSerializer(),
            400: OpenApiResponse(description="Bad Request"),
            403: OpenApiResponse(description="Authentication credentials were not provided"),
        },
        tags=["Profile"],
    ),
)
class ProfileRetrieveUpdateView(RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(User, id=self.request.user.id)
