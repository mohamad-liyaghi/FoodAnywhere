from django.db import IntegrityError
from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)
from users.models import User
from active_sessions.enums import LoginDeviceType, LoginBrowserType


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "first_name", "last_name"]

    def create(self, validated_data):
        try:
            return User.objects.create_user(**validated_data)
        except IntegrityError:
            raise serializers.ValidationError("A user with similar email already exists.")


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "balance"]
        read_only_fields = ["email", "balance"]


class UserPasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128)
    new_password = serializers.CharField(max_length=128, min_length=8)

    @staticmethod
    def _validate_old_password(value: str, instance: User) -> str:
        if not instance.check_password(value):
            raise serializers.ValidationError("Invalid password were provided.")
        return value

    @staticmethod
    def _validate_new_password(value: str, instance: User) -> str:
        if instance.check_password(value):
            raise serializers.ValidationError("New password cannot be the same as the old password.")
        return value

    def update(self, instance: User, validated_data: dict) -> User:
        old_password = validated_data["old_password"]
        new_password = validated_data["new_password"]

        self._validate_old_password(old_password, instance)
        self._validate_new_password(new_password, instance)

        instance.set_password(new_password)
        instance.save()
        return instance


class AccessTokenObtainSerializer(TokenObtainPairSerializer):
    device_type = serializers.ChoiceField(choices=LoginDeviceType.choices)
    browser_type = serializers.ChoiceField(choices=LoginBrowserType.choices)


class AccessTokenRefreshSerializer(TokenRefreshSerializer):
    device_type = serializers.ChoiceField(choices=LoginDeviceType.choices)
    browser_type = serializers.ChoiceField(choices=LoginBrowserType.choices)
