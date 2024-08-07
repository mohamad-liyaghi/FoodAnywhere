from django.urls import path, include
from transactions.views.deposits import DepositListCreateView, DepositStatusCheckView

app_name = "transactions"

WITHDRAWAL_URLS = []
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
