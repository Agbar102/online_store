from django.contrib import admin
from .models import Category, SubCategory, Items, Favorite


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    search_fields = ('name',)


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'order')



@admin.register(Items)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'subcategory', 'price', 'is_available', 'order')
    ordering = ('-id',)
    list_filter = ('subcategory', 'is_available')
    search_fields = ('title', 'production', 'model')

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'items', 'created_at')