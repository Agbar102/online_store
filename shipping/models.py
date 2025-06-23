from django.db import models


class Shipping(models.Model):
    class CourierService(models.IntegerChoices):
        Cdek = 1, "Cdek"
        Express = 2, "Express"
        LOCAL = 3, "Местная доставка"
        OTHER = 4, "Другое"

    class DeliveryStatus(models.IntegerChoices):
        PENDING = 1, "Ожидает"
        IN_TRANSIT = 2, "В пути"
        DELIVERED = 3, "Доставлено"
        CANCELLED = 4, "Отменено"

    client_name = models.CharField(verbose_name="Имя получателя",max_length=255)
    address = models.TextField(verbose_name="Адрес доставки")
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    courier = models.IntegerField(choices=CourierService.choices, default=CourierService.LOCAL, verbose_name="Служба доставки")
    cost = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Стоимость доставки")
    tracking_number = models.CharField(max_length=100, blank=True, null=True, verbose_name="Трек-номер")
    status = models.IntegerField(choices=DeliveryStatus.choices, default=DeliveryStatus.PENDING, verbose_name="Статус доставки")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.client_name} - {self.status}"

    def is_delivered(self):
        return self.status == self.DeliveryStatus.DELIVERED

    class Meta:
        verbose_name = "Доставка"
        verbose_name_plural = "Доставки"