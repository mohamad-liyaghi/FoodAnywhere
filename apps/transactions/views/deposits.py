from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema_view, OpenApiResponse, extend_schema
from transactions.models import Transaction
from transactions.enums import TransactionStatus, TransactionType
from transactions.serializers import DepositSerializer
from transactions.permissions import DepositLimitPermission


@extend_schema_view(
    post=extend_schema(
        summary="Create a deposit",
        description="Create a deposit for the user",
        responses={
            201: DepositSerializer(),
            400: OpenApiResponse(description="Bad Request"),
            403: OpenApiResponse(description="Unauthorized or is spam [3 deposits in 20 minutes]"),
        },
        tags=["Deposits"],
    ),
    get=extend_schema(
        summary="List deposits",
        description="List all deposits for the user",
        responses={
            200: DepositSerializer(many=True),
            403: OpenApiResponse(description="Unauthorized"),
        },
        tags=["Deposits"],
    ),
)
class DepositListCreateView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, DepositLimitPermission)
    serializer_class = DepositSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Transaction.objects.select_related("user").filter(user=self.request.user, type=TransactionType.DEPOSIT)


@extend_schema_view(
    post=extend_schema(
        summary="Check deposit status and update status",
        description="Check deposit status by uuid",
        responses={
            200: "OK",
            400: OpenApiResponse(description="Bad Request"),
            403: OpenApiResponse(description="Unauthorized"),
            404: OpenApiResponse(description="Pending Not Found"),
        },
        tags=["Deposits"],
    ),
)
class DepositStatusCheckView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, request):
        return get_object_or_404(
            Transaction,
            uuid=self.kwargs.get("uuid"),
            user=request.user,
            type=TransactionType.DEPOSIT,
        )

    def get(self, request, *args, **kwargs):
        deposit = self.get_object(request)
        if request.query_params.get("set_status", "ok") == "ok":
            deposit.status = TransactionStatus.SUCCESS
            deposit.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
