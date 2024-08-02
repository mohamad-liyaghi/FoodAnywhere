from django.urls import path, include
from users.views.auth import (
    UserRegisterView,
    AccessTokenObtainView,
    AccessTokenRefreshView,
)
from users.views.profile import ProfileRetrieveUpdateView

app_name = "users"


AUTH_URLS = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("token/access/", AccessTokenObtainView.as_view(), name="access-token"),
    path("token/refresh/", AccessTokenRefreshView.as_view(), name="refresh-token"),
]
PROFILE_URLS = [
    path("", ProfileRetrieveUpdateView.as_view(), name="profile"),
]

urlpatterns = [
    path("auth/", include(AUTH_URLS)),
    path("profile/", include(PROFILE_URLS)),
]
