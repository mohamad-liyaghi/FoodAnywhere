from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema_view, OpenApiResponse, extend_schema
from transactions.models import Transaction
from transactions.enums import TransactionType
from transactions.permissions import WithdrawalLimitPermission
from transactions.serializers import WithdrawalSerializer


@extend_schema_view(
    post=extend_schema(
        summary="Create a withdrawal request",
        description="Create a withdrawal request for the user",
        responses={
            201: WithdrawalSerializer(),
            400: OpenApiResponse(description="Bad Request"),
            403: OpenApiResponse(description="Unauthorized or is spam [3 pending withdrawals]"),
        },
        tags=["Withdrawals"],
    ),
    get=extend_schema(
        summary="List all transactions",
        description="List all transactions for the user",
        responses={
            200: WithdrawalSerializer(many=True),
            403: OpenApiResponse(description="Unauthorized"),
        },
        tags=["Withdrawals"],
    ),
)
class WithdrawalListCreateView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, WithdrawalLimitPermission)
    serializer_class = WithdrawalSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["user"] = self.request.user
        return context

    def get_queryset(self):
        return (
            Transaction.objects.select_related("user")
            .filter(user=self.request.user, type=TransactionType.WITHDRAWAL)
            .order_by("-created_at")
        )
