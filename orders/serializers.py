from rest_framework import serializers
from .models import OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_title', 'quantity', 'price', 'status']
        read_only_fields = ['user', 'created_at', 'total_price']

    def validate(self, attrs):
        items = attrs.get('items', [])
        if not items:
            raise serializers.ValidationError('Нельзя оформить пустой заказ.')

        for item in items:
            if item.quantity < 1:
                raise serializers.ValidationError("Количество товара должно быть больше 0.")
            if not item.product.is_available:
                raise serializers.ValidationError(f"Товар {item.product.title} недоступен.")

        return attrs



