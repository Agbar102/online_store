from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import permissions, generics, status
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from shipping.serializers import ShippingSerializer
from .serializers import OrderSerializer, SingleProductOrderSerializer, CheckoutSerializer
from .models import Order
import logging

logger = logging.getLogger(__name__)


class UserOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')


class SingleProductOrderView(generics.GenericAPIView):
    serializer_class = SingleProductOrderSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=SingleProductOrderSerializer,
        responses={
            201: inline_serializer(
                name="SingleProductOrderResponse",
                fields={
                    "message": serializers.CharField(),
                    "order_id": serializers.IntegerField(),
                    "product": serializers.CharField(),
                    "quantity": serializers.IntegerField(),
                    "product_total": serializers.FloatField(),
                    "shipping_cost": serializers.FloatField(),
                    "total_price": serializers.FloatField(),
                    "tracking_number": serializers.CharField()
                }
            )
        }
    )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        result = serializer.save()

        return Response({
            "message": "Заказ оформлен",
            "order_id": result["order"].id,
            "product": result["item"].product.title,
            "quantity": result["item"].quantity,
            "product_total": result["item"].get_total_price(),
            "shipping_cost": result["shipping"].cost,
            "total_price": result["order"].total_price,
            "tracking_number": result["shipping"].tracking_number
        }, status=status.HTTP_201_CREATED)


class CheckoutView(generics.GenericAPIView):
    serializer_class = CheckoutSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=CheckoutSerializer,
        responses={
            201: inline_serializer(
                name="CheckoutResponse",
                fields={
                    "message": serializers.CharField(),
                    "order_id": serializers.IntegerField(),
                    "products_total": serializers.FloatField(),
                    "shipping_cost": serializers.FloatField(),
                    "total_price": serializers.FloatField(),
                    "shipping": ShippingSerializer()
                }
            )
        }
    )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        result = serializer.save()

        return Response({
            "message": "Заказ оформлен",
            "order_id": result["order"].id,
            "products_total": result["products_total"],
            "shipping_cost": result["shipping"].cost,
            "total_price": result["order"].total_price,
            "shipping": ShippingSerializer(result["shipping"]).data
        }, status=status.HTTP_201_CREATED)

