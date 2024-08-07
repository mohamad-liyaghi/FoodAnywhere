from django.urls import path, include
from transactions.views.deposits import DepositListCreateView

app_name = "transactions"

WITHDRAWAL_URLS = []
DEPOSIT_URLS = [
    path("", DepositListCreateView.as_view(), name="deposit-list-create"),
]

urlpatterns = [
    path("withdrawals/", include(WITHDRAWAL_URLS)),
    path("deposits/", include(DEPOSIT_URLS)),
]
