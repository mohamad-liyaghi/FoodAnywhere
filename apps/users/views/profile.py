from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema_view, OpenApiResponse, extend_schema
from users.models import User
from users.serializers import UserProfileSerializer, UserPasswordChangeSerializer


@extend_schema_view(
    get=extend_schema(
        summary="Retrieve user profile",
        description="Retrieve user profile information",
        responses={
            200: UserProfileSerializer(),
            403: OpenApiResponse(description="Authentication credentials were not provided"),
        },
        tags=["Profile"],
    ),
    put=extend_schema(
        summary="Update user profile",
        description="Update user profile information",
        responses={
            200: UserProfileSerializer(),
            400: OpenApiResponse(description="Bad Request"),
            403: OpenApiResponse(description="Authentication credentials were not provided"),
        },
        tags=["Profile"],
    ),
    patch=extend_schema(
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


@extend_schema_view(
    post=extend_schema(
        summary="Change Password",
        description="""Change Password.""",
        request=UserPasswordChangeSerializer,
        responses={
            200: OpenApiResponse(description="Password changed"),
            400: OpenApiResponse(description="Invalid Password/Same password"),
            401: OpenApiResponse(description="Unauthorized"),
        },
        tags=["Profile"],
    ),
)
class PasswordChangeView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserPasswordChangeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.update(instance=request.user, validated_data=serializer.validated_data)
            return Response("Password changed successfully", status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
