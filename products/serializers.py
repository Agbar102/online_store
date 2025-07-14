from rest_framework import serializers
from django.db.models import Avg
from .models import Items, Favorite, Category, SubCategory


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'order']


class SubCategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'order', 'category', 'category_name']


class PublicItemSerializer(serializers.ModelSerializer):
    subcategory = serializers.CharField(source='subcategory.name' , read_only=True)

    class Meta:
        model = Items
        fields = ['id', 'image', 'title', 'description', 'slug', 'price', 'production', 'model', 'is_available', 'color', 'subcategory']

    def to_representation(self, instance):
        reviews = instance.reviews.all()
        voice = reviews.count()
        average_rating = reviews.aggregate(avg=Avg('rating'))['avg'] if reviews else  None

        representation = super().to_representation(instance)

        representation['average_rating'] = average_rating
        representation['voice'] = voice
        return representation


class AdminItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = '__all__'

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Цена не может быть отрицательной")
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("Количество на складе не может быть отрицательным")
        return value

    def validate(self, data):
        if data.get("is_active") and data.get("stock", 0) <= 0:
            raise serializers.ValidationError("Нельзя активировать товар без наличия на складе")
        return data


class FavoriteSerializer(serializers.ModelSerializer):
    items = PublicItemSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'user', 'items', 'created_at']
        read_only_fields = ['user']


class FavoriteCreateSerializer(serializers.ModelSerializer):
    items = serializers.PrimaryKeyRelatedField(queryset=Items.objects.all())

    class Meta:
        model = Favorite
        fields = ['items']

    def validate_items(self, items):
        if not items.is_active:
            raise serializers.ValidationError("Этот товар недоступен для избранного")
        user = self.context['request'].user
        if Favorite.objects.filter(user=user, items=items).exists():
            raise serializers.ValidationError("Продукт уже в избранном")
        return items

