from django.db import models
from django.contrib.auth import get_user_model
from products.models import SubCategory, Items
from shipping.models import Shipping

User = get_user_model()

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    shipping = models.OneToOneField(Shipping, on_delete=models.CASCADE, null=True, blank=True, related_name='order')
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-created_at']

    def __str__(self):
        return f"Заказ #{self.id} от {self.user}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Items, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField("Количество",default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_total_price(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.product.title} * {self.quantity}"

    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказа"