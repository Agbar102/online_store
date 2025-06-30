from django.shortcuts import render
from rest_framework import viewsets, permissions
from .serializers import OrderItemSerializer
from .permissions import IsOwnerOrAdminForOrder
from .models import Order, OrderItem
from .tasks import send_order_email


class OrderItemViewSet(viewsets.ModelViewSet):
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdminForOrder]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        order = serializer.save(user=self.request.user)
        send_order_email.delay(order.user.email, order.id)