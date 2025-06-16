from django.db import models
from django.contrib.auth import get_user_model
from products.models import SubCategory

User = get_user_model()

class Cart(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="carts")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Коризины"

    def __str__(self):
        return f"Корзина {self.user}"

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.title}"

    def total_price(self):
        return self.product.price * self.quantity

    class Meta:
        verbose_name = "Товар в корзине"
        verbose_name_plural = "Товары в корзине"