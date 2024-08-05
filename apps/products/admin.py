from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "restaurant",
        "price",
        "quantity",
        "max_quantity_per_order",
        "type",
    ]
    list_filter = ["type"]
    search_fields = ["name", "restaurant__name"]
    ordering = ["type", "price"]
    readonly_fields = ["uuid"]
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "uuid",
                    "restaurant",
                    "name",
                    "description",
                    "price",
                    "quantity",
                    "max_quantity_per_order",
                    "type",
                ]
            },
        )
    ]
    raw_id_fields = ["restaurant"]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("restaurant")
