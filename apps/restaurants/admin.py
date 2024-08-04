from django.contrib import admin
from .models import Restaurant


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ["name", "owner", "status", "created_at"]
    list_filter = ["status", "created_at"]
    search_fields = ["name", "owner__username"]
    date_hierarchy = "created_at"
    ordering = ["-created_at"]
    readonly_fields = ["uuid", "created_at", "updated_at"]
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "uuid",
                    "owner",
                    "name",
                    "description",
                    "phone",
                    "location",
                    "longitude",
                    "latitude",
                    "status",
                ]
            },
        ),
        (
            "Date Information",
            {"fields": ["created_at", "updated_at"], "classes": ["collapse"]},
        ),
    ]
    raw_id_fields = ["owner"]
    actions = ["approve_restaurants", "deny_restaurants", "cancel_restaurants"]

    def approve_restaurants(self, request, queryset):
        queryset.update(status="a")

    approve_restaurants.short_description = "Approve selected restaurants"

    def deny_restaurants(self, request, queryset):
        queryset.update(status="d")

    deny_restaurants.short_description = "Deny selected restaurants"

    def cancel_restaurants(self, request, queryset):
        queryset.update(status="c")

    cancel_restaurants.short_description = "Cancel selected restaurants"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("owner")
