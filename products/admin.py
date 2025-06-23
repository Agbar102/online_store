from django.contrib import admin
from .models import Category, SubCategory, Items


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    search_fields = ('name',)


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'order')



@admin.register(Items)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'subcategory', 'price', 'is_available', 'order')
    list_filter = ('subcategory', 'is_available')
    search_fields = ('title', 'production', 'model')
