from django.urls import path
from active_sessions.views import ActiveSessionListView

app_name = "active_sessions"

urlpatterns = [
    path("", ActiveSessionListView.as_view(), name="list"),
]
