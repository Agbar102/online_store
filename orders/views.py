from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import OrderSerializer, OrderItemSerializer
from .permissions import IsOwnerOrAdminForOrder
from .models import Order, OrderItem
from .tasks import send_order_email
from cart.models import Cart
import logging

logger = logging.getLogger(__name__)



class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdminForOrder]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.role == 'admin':
            return Order.objects.all().order_by('-created_at')
        return Order.objects.filter(user=user).order_by('-created_at')

    def perform_create(self, serializer):
        order = serializer.save()
        send_order_email.delay(order.user.email, order.id)


class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart = Cart.objects.prefetch_related('items').get(user=request.user)
        if not cart.items.exists():
            return Response({"error": "Корзина пуста"}, status=400)

        order = Order.objects.create(user=request.user)
        total = 0

        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
            total += cart_item.get_total_price()

        order.total_price = total
        order.save()

        cart.items.all().delete()

        return Response({"message": "Заказ оформлен", "order_id": order.id}, status=201)