from django.contrib import admin
from .models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "restaurant",
        "status",
        "created_at",
        "updated_at",
        "total_price",
    )
    list_filter = ("status", "restaurant")
    search_fields = ("user__email", "restaurant__name")
    date_hierarchy = "created_at"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user", "restaurant")


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order",
        "product",
        "quantity",
        "price",
        "created_at",
        "updated_at",
    )
    list_filter = ("order", "product")
    search_fields = ("order__user__email", "product__name")
    date_hierarchy = "created_at"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("order", "product")
