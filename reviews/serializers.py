from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'product', 'user', 'rating', 'text', 'created_at']
        read_only_fields = ['created_at']

        def validate(self, data):
            user = self.context['request'].user
            product = data['product']
            if Review.objects.filter(user=user, product=product).exists():
                raise serializers.ValidationError("Вы уже оставляли отзыв на этот товар.")
            return data
