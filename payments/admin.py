from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "order",
        "amount",
        "provider",
        "status",
        "created_at",
    )
    list_filter = ("provider", "status", "created_at")
    search_fields = ("user__email", "order__id", "provider_payment_id")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")