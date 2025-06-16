from django.contrib import admin
from .models import Cart, CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created_at", "total_price_display")
    list_filter = ("created_at",)

    def total_price_display(self, obj):
        return obj.total_price()
    total_price_display.short_description = "Итоговая сумма"


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("id", "cart", "quantity", "total_price_display")
    list_filter = ("cart__created_at",)

    def total_price_display(self, obj):
        return obj.total_price()
    total_price_display.short_description = "Итоговая сумма"
