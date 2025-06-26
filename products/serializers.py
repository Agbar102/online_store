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
    subcategory = serializers.CharField(source='subcategory.name' ,read_only=True)


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


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['id', 'user', 'product', 'created_at']
        read_only_fields = ['user']

    def validate(self, data):
        user = self.context['request'].user
        product = data['product']
        if Favorite.objects.filter(user=user, product=product).exists():
            raise serializers.ValidationError("Продукт уже в избранном")
        return data
