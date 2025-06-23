from django.contrib import admin
from .models import Shipping


@admin.register(Shipping)
class ShippingAdmin(admin.ModelAdmin):
    list_display = (
        "client_name",
        "courier",
        "cost",
        "status",
        "tracking_number",
        "created_at",
    )
    list_filter = ("courier", "status", "created_at")
    search_fields = ("client_name", "tracking_number", "address", "postal_code")
    readonly_fields = ("created_at", "updated_at")