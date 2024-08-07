from django.contrib import admin
from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "amount", "type", "status"]
    list_filter = ["type", "status"]
    search_fields = ["user__email", "user__email"]
    ordering = ["-created_at"]
    readonly_fields = ["uuid", "created_at", "updated_at"]
    fieldsets = (
        (None, {"fields": ("uuid", "user", "amount", "type", "status")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )
    add_fieldsets = ((None, {"fields": ("user", "amount", "type", "status")}),)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user")
