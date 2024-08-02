from django.contrib import admin
from .models import ActiveSession


@admin.register(ActiveSession)
class ActiveSessionAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "device_type",
        "browser_type",
        "ip_address",
        "date",
    ]
    list_filter = ["device_type", "browser_type"]
    search_fields = ["user__email", "ip_address"]
    ordering = ["-date"]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user")
