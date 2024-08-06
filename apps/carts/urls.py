from django.urls import path
from carts.views import CartListCreateView

app_name = "carts"

urlpatterns = [
    path("", CartListCreateView.as_view(), name="list-create"),
]
