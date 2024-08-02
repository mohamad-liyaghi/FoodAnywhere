from rest_framework import serializers
from active_sessions.models import ActiveSession


class ActiveSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActiveSession
        fields = ["date", "device_type", "browser_type", "ip_address"]
