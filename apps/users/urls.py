from django.urls import path, include
from users.views.auth import UserRegisterView, AccessTokenObtainView

app_name = "users"


AUTH_URLS = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("token/access/", AccessTokenObtainView.as_view(), name="access-token"),
]
PROFILE_URLS = []

urlpatterns = [
    path("auth/", include(AUTH_URLS)),
    path("profile/", include(PROFILE_URLS)),
]
