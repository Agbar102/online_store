
from rest_framework import serializers
from products.models import Items
from cart.models import Cart, CartItem

class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.title', read_only=True)
    price = serializers.DecimalField(source='product.price', read_only=True, max_digits=10, decimal_places=2)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_name', 'price', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'created_at', 'items']


class CartItemCreateSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Items.objects.all())
    quantity = serializers.IntegerField(min_value=1, default=1)

    def validate_product(self, product):
        if not product.is_active:
            raise serializers.ValidationError('Этот товар недоступен для заказа')
        return product

    def validate(self, data):
        product = data['product']
        quantity = data['quantity']

        if quantity > product.stock:
            raise serializers.ValidationError(f"Доступно только {product.stock} шт.")
        return data


    def save(self, **kwargs):
        user = self.context['request'].user
        cart, _ = Cart.objects.get_or_create(user=user)
        product = self.validated_data['product']
        quantity = self.validated_data['quantity']

        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            item.quantity += quantity
        else:
            item.quantity = quantity
        item.save()
        return item


class CartItemUpdateSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Items.objects.all())
    quantity = serializers.IntegerField(min_value=0)

    def validate(self, data):
        product = data['product']
        quantity = data['quantity']

        if quantity > product.stock:
            raise serializers.ValidationError(f"Доступно только {product.stock} шт.")
        return data

    def save(self, **kwargs):
        user = self.context['request'].user
        cart, _ = Cart.objects.get_or_create(user=user)
        product = self.validated_data['product']
        quantity = self.validated_data['quantity']

        try:
            item = CartItem.objects.get(cart=cart, product=product)
        except CartItem.DoesNotExist:
            raise serializers.ValidationError("Этот товар не в корзине")

        if quantity == 0:
            item.delete()
            return None

        item.quantity = quantity
        item.save()
        return item