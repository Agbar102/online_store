from rest_framework import permissions, generics
from rest_framework.views import APIView
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


class SingleProductOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SingleProductOrderSerializer(data=request.data, context={"request": request})
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
        }, status=201)


class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CheckoutSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        result = serializer.save()

        return Response({
            "message": "Заказ оформлен",
            "order_id": result["order"].id,
            "products_total": result["products_total"],
            "shipping_cost": result["shipping"].cost,
            "total_price": result["order"].total_price,
            "shipping": ShippingSerializer(result["shipping"]).data
        }, status=201)