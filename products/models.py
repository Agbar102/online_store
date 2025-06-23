from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    name = models.CharField("Категории", max_length=255)
    order = models.PositiveIntegerField("Порядок", default=1)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ("order",)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories")
    name = models.CharField("Подкатегория", max_length=255)
    order = models.PositiveIntegerField("Порядок", default=1)

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"
        ordering = ("order",)

    def __str__(self):
        return self.name

class Items(models.Model):
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name="items")
    image = models.ImageField("Главаная картина товара", upload_to="image_items", null=True, blank=True)
    title = models.CharField("Название товара", max_length=255)
    description = models.TextField("Описание товара", null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, verbose_name="Slug", null=True, blank=True)
    price = models.DecimalField("Цена", max_digits=8, decimal_places=2, null=True, blank=True)
    production = models.CharField("Производство", max_length=255, null=True, blank=True)
    model = models.CharField("Модель", max_length=255, null=True, blank=True)
    is_available = models.BooleanField("Наличие", default=False)
    color = models.CharField("Цвет", max_length=20, null=True, blank=True)
    order = models.PositiveIntegerField("Порядок", default=1)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ("order",)

    def __str__(self):
        return self.title


class Favorite(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="favorites")
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="favorited_by")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')


