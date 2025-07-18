from rest_framework import serializers
from orders.models import Order
from payments.models import Payment


class CheckoutSessionSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    provider = serializers.ChoiceField(choices=Payment.PaymentProvider.choices)

    def validate_order_id(self, value):
        user = self.context['request'].user
        if not Order.objects.filter(id=value, user=user).exists():
            raise serializers.ValidationError("Заказ не найден или не принадлежит пользователю.")
        return value