from django.urls import path
from locations.views import LocationListCreateView

app_name = "locations"

urlpatterns = [
    path("", LocationListCreateView.as_view(), name="list-create"),
]
