from rest_framework import serializers
from transactions.models import Transaction


class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ("uuid", "amount", "status", "created_at", "updated_at", "user")
        read_only_fields = ("uuid", "status", "created_at", "updated_at", "user")
