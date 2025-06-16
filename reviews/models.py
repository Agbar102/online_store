from django.db import models
from products.models import SubCategory
from django.contrib.auth import get_user_model

User = get_user_model()

class Review(models.Model):
    RATE_CHOICE = (
        (1, "Ужасно"),
        (2, "Плохо"),
        (3, "Хорошо"),
        (4, "Превосходно"),
    )
    product = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='reviews')

    rating = models.PositiveSmallIntegerField(choices=RATE_CHOICE)
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        unique_together = ('product', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f"Отзыв {self.rating} от {self.user} на {self.product}"
