from django.urls import path, include
from users.views.auth import UserRegisterView

app_name = "users"


AUTH_URLS = [path("register/", UserRegisterView.as_view(), name="register")]
PROFILE_URLS = []

urlpatterns = [
    path("auth/", include(AUTH_URLS)),
    path("profile/", include(PROFILE_URLS)),
]
