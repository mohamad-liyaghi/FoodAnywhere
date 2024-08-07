from django.urls import path, include
from transactions.views.deposits import DepositListCreateView, DepositStatusCheckView
from transactions.views.withdrawals import WithdrawalListCreateView

app_name = "transactions"

WITHDRAWAL_URLS = [
    path("", WithdrawalListCreateView.as_view(), name="withdrawal-list-create"),
]
DEPOSIT_URLS = [
    path("", DepositListCreateView.as_view(), name="deposit-list-create"),
    path(
        "status/<uuid:uuid>/",
        DepositStatusCheckView.as_view(),
        name="deposit-status-check",
    ),
]

urlpatterns = [
    path("withdrawals/", include(WITHDRAWAL_URLS)),
    path("deposits/", include(DEPOSIT_URLS)),
]
