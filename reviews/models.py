from django.db import models
from products.models import Items
from django.contrib.auth import get_user_model

User = get_user_model()

class Review(models.Model):
    class RateChoice(models.IntegerChoices):
        BAD = 1, "Ужасно"
        POOR = 2, "Плохо"
        GOOD = 3, "Хорошо"
        EXCELLENT = 4, "Превосходно"

    product = models.ForeignKey(Items, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='reviews')

    rating = models.IntegerField(choices=RateChoice.choices, default=RateChoice.GOOD)
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['-created_at']

    def __str__(self):
        return f"Отзыв {self.rating} от {self.user} на {self.product}"
