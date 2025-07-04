from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from products.models import Items

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
        product_id = request.data.get('product')
        quantity = int(request.data.get('quantity', 1))

        if not product_id:
            return Response({"error": "Нужен product ID"}, status=400)

        try:
            product = Items.objects.get(id=product_id)
        except Items.DoesNotExist:
            return Response({"error": "Товар не найден"}, status=404)

        cart = self.get_user_cart(request.user)

        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        item.quantity += quantity if not created else 0
        item.save()

        return Response({"message": "Товар добавлен в корзину"}, status=201)

        @action(detail=True, methods=['delete'])
        def remove_item(self, request, pk=None):
            cart = self.get_user_cart(request.user)
            try:
                item = CartItem.objects.get(cart=cart, id=pk)
                item.delete()
                return Response({"message": "Товар удален"}, status=204)
            except CartItem.DoesNotExist:
                return Response({"error": "Товар не найден"}, status=404)