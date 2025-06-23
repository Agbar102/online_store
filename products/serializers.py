from rest_framework import serializers
from .models import Items, Favorite


class PublicItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = ['id', 'image', 'title', 'description', 'slug', 'price', 'production', 'model', 'is_available', 'color',]


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
