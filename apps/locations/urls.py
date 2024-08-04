from django.urls import path
from locations.views import LocationListCreateView, LocationUpdateView

app_name = "locations"

urlpatterns = [
    path("", LocationListCreateView.as_view(), name="list-create"),
    path("<uuid:uuid>/", LocationUpdateView.as_view(), name="update"),
]
