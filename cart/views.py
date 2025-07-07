from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer, CartItemCreateSerializer, CartItemUpdateSerializer


class CartViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def get_user_cart(self, user):
        cart, _ = Cart.objects.get_or_create(user=user)
        return cart

    def list(self, request):
        cart = self.get_user_cart(request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


    @action(detail=False, methods=['post'])
    def add_item(self, request):
        serializer = CartItemCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        item = serializer.save()
        return Response(CartItemSerializer(item).data, status=status.HTTP_201_CREATED)


    @action(detail=False, methods=['post'])
    def update_item(self, request):
        serializer = CartItemUpdateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        item = serializer.save()
        if item is None:
            return Response({"message": "Товар удалён из корзины"}, status=status.HTTP_204_NO_CONTENT)
        return Response(CartItemSerializer(item).data)


    @action(detail=True, methods=['delete'])
    def remove_item(self, request, pk=None):
        cart = self.get_user_cart(request.user)
        try:
            item = CartItem.objects.get(cart=cart, id=pk)
            item.delete()
            return Response({"message": "Товар удален"}, status=204)
        except CartItem.DoesNotExist:
            return Response({"error": "Товар не найден"}, status=404)