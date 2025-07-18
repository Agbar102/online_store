from rest_framework import serializers
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

        delivered_shippings = Shipping.objects.filter(
            user=user,
            status=Shipping.DeliveryStatus.DELIVERED
        )

        has_delivered_product = False
        for shipping in delivered_shippings:
            for order in shipping.order.all():
                if order.items.filter(product=product).exists():
                    has_delivered_product = True
                    break

        if not has_delivered_product:
            raise serializers.ValidationError("Вы можете оставить отзыв только после доставки этого товара.")

        return data

    def validate_rating(self, rating):
        if not 1 <= rating <= 10:
            raise serializers.ValidationError("Рейтинг должен быть от 1 до 10.")
        return rating

