from django.contrib.gis.admin import GISModelAdmin
from django.contrib import admin
from .models import Location


@admin.register(Location)
class LocationAdmin(GISModelAdmin):
    list_display = ("user", "title", "location", "is_primary", "created_at")
    search_fields = ("title",)
    ordering = ("created_at",)
    list_filter = ("created_at", "updated_at")
    date_hierarchy = "created_at"
    readonly_fields = ("uuid", "created_at", "updated_at")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "user",
                    "uuid",
                    "title",
                    "location",
                    "longitude",
                    "latitude",
                    "created_at",
                    "updated_at",
                    "description",
                    "is_primary",
                )
            },
        ),
    )
    map_width = 800
    map_height = 500
    map_srid = 4326
    modifiable = False
    openlayers_url = "https://cdnjs.cloudflare.com/ajax/libs/openlayers/2.13.1/OpenLayers.js"
    openlayers_default_lon = 5
    openlayers_default_lat = 40
    openlayers_default_zoom = 4
    openlayers_layers = [
        ("Google Physical", "TERRAIN"),
        ("Google Streets", "ROADMAP"),
        ("Google Hybrid", "HYBRID"),
        ("Google Satellite", "SATELLITE"),
    ]
    openlayers_map_srid = 4326
    openlayers_units = "m"
    openlayers_max_zoom = 19
    openlayers_min_zoom = 3
    openlayers_zoom = 10
    openlayers_projection = "EPSG:4326"
    openlayers_display_srid = 4326
    openlayers_wrldparams = {
        "attribution": "Your attribution",
        "maxExtent": "-180,-90,180,90",
        "restrictedExtent": "-180,-90,180,90",
        "numZoomLevels": 21,
        "maxResolution": "1.40625",
        "units": "degrees",
        "projection": "EPSG:4326",
        "displayProjection": "EPSG:4326",
        "controls": [
            "LayerSwitcher",
        ],
    }

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user")
