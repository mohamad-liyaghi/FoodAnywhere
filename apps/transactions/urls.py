from django.urls import path, include

app_name = "transactions"

WITHDRAWAL_URLS = []
DEPOSIT_URLS = []

urlpatterns = [
    path("withdrawals/", include(WITHDRAWAL_URLS)),
    path("deposits/", include(DEPOSIT_URLS)),
]
