from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
        path("download/", SpectacularAPIView.as_view(), name="download-schema"),
        path(
            "",
            SpectacularSwaggerView.as_view(url_name="download-schema"),
            name="swagger-ui",
        ),
    ]
