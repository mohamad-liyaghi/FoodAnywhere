from django.contrib import admin
from django.conf import settings
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "email",
        "first_name",
        "last_name",
        "balance",
        "is_active",
        "is_staff",
        "date_joined",
    ]
    search_fields = ["email", "first_name", "last_name"]
    list_filter = ["is_active", "is_staff"]
    readonly_fields = ["date_joined", "password"]

    if not settings.DEBUG:
        readonly_fields.append("balance")

    fieldsets = [
        (
            None,
            {
                "fields": [
                    "email",
                ]
            },
        ),
        (
            "Personal info",
            {"fields": ["first_name", "last_name", "balance"]},
        ),
        ("Permissions", {"fields": ["is_active", "is_staff"]}),
        ("Important dates", {"fields": ["date_joined"]}),
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": [
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                ],
            },
        ),
    ]
    ordering = ["email"]
    filter_horizontal = []
    actions = ["activate_users", "deactivate_users", "make_staff", "make_superuser"]

    def activate_users(self, request, queryset):
        queryset.update(is_active=True)

    def deactivate_users(self, request, queryset):
        queryset.update(is_active=False)

    activate_users.short_description = "Activate selected users"
    deactivate_users.short_description = "Deactivate selected users"
