from rest_framework import serializers
from .models import Shipping


class ShippingSerializer(serializers.ModelSerializer):
    courier_name = serializers.CharField(source='get_courier_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Shipping
        fields = [
            'id', 'client_name', 'address', 'city', 'postal_code', 'country',
            'courier', 'courier_name', 'cost', 'tracking_number',
            'status', 'status_display'
        ]
        read_only_fields = ['user', 'cost', 'tracking_number', 'status']

    def create(self, validated_data):
        courier = validated_data.get("courier")

        if courier == Shipping.CourierService.Cdek:
            cost = 200
        elif courier == Shipping.CourierService.Express:
            cost = 400
        elif courier == Shipping.CourierService.LOCAL:
            cost = 100
        else:
            cost = 150

        validated_data["cost"] = cost
        return super().create(validated_data)