from rest_framework import serializers

from orders.models import OrderItem
from .models import Review
from shipping.models import Shipping

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'product', 'rating', 'text', 'created_at']
        read_only_fields = ['created_at', 'user']

    def validate(self, data):
        user = self.context['request'].user
        product = data['product']

        if Review.objects.filter(user=user, product=product).exists():
            raise serializers.ValidationError("Вы уже оставляли отзыв на этот товар.")

        order_items = OrderItem.objects.filter(
            product=product,
            order__user=user,
            order__shipping__status=Shipping.DeliveryStatus.DELIVERED
        )

        if not order_items:
            raise serializers.ValidationError("Вы можете оставить отзыв только после доставки этого товара.")

        return data

    def validate_rating(self, rating):
        if not 1 <= rating <= 10:
            raise serializers.ValidationError("Рейтинг должен быть от 1 до 10.")
        return rating

