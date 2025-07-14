from rest_framework import serializers
from payments.models import Payment


class CheckoutSessionSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    provider = serializers.ChoiceField(choices=Payment.PaymentProvider.choices)