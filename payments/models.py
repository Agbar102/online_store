from django.db import models
from django.contrib.auth import get_user_model
from orders.models import Order

User = get_user_model()

class Payment(models.Model):
    class PaymentProvider(models.TextChoices):
        STRIPE = "stripe", "Stripe"
        MBANK = "mbank", "Mbank"
        OPTIMA = "optimabank", "OptimaBank"
        BAKAI = "bakaibank", "BakaiBank"
        OTHER = "other", "Другое"

    class PaymentStatus(models.TextChoices):
        PENDING = "pending", "Ожидание"
        PAID = "paid", "Оплачено"
        FAILED = "failed", "Ошибка"
        REFUNDED = "refunded", "Возврат"
        CANCELED = "canceled", "Отменено"

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="payments")
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="payments")

    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма")
    provider = models.CharField(max_length=20, choices=PaymentProvider.choices, default=PaymentProvider.STRIPE, verbose_name="Платёжная система")
    status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING, verbose_name="Статус")
    provider_payment_id = models.CharField(max_length=255, blank=True, null=True, verbose_name="ID платежа в системе")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Платёж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return f"{self.id} | {self.order} | {self.status}"
