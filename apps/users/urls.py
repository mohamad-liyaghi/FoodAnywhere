from django.urls import path, include

app_name = "users"


AUTH_URLS = []
PROFILE_URLS = []

urlpatterns = [
    path("auth/", include(AUTH_URLS)),
    path("profile/", include(PROFILE_URLS)),
]
