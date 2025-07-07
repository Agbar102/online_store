from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from products.models import Items
from django.contrib.auth import get_user_model

User = get_user_model()

class Review(models.Model):
    product = models.ForeignKey(Items, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='reviews')

    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], default=5, verbose_name="Оценка (1-10)")
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['-created_at']

    def __str__(self):
        return f"Отзыв {self.rating} от {self.user} на {self.product}"
