from rest_framework import serializers
from cart.models import Cart
from products.models import Items
from shipping.serializers import ShippingSerializer
from .tasks import send_order_email
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source='product.title', read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(source='product', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product_id', 'product_title', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    shipping = ShippingSerializer(read_only=True)
    shipping_status = serializers.CharField(source='shipping.get_status_display', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'created_at', 'total_price', 'shipping_status' , 'shipping', 'items']


class OrderItemCreateSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Items.objects.all())
    quantity = serializers.IntegerField(min_value=1)

    def validate_product(self, value):
        if not value.is_active:
            raise serializers.ValidationError("Товар не активен")
        return value


class SingleProductOrderSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Items.objects.all())
    quantity = serializers.IntegerField(min_value=1)
    shipping = ShippingSerializer()

    def validate(self, data):
        product = data['product']
        quantity = data['quantity']

        if not product.is_active:
            raise serializers.ValidationError("Товар не активен")

        if quantity > product.stock:
            raise serializers.ValidationError(f"Доступно только {product.stock} шт.")

        return data

    def create(self, validated_data):
        request = self.context['request']
        user = request.user

        product = validated_data['product']
        quantity = validated_data['quantity']
        shipping_data = validated_data['shipping']

        shipping_serializer = ShippingSerializer(data=shipping_data)
        shipping_serializer.is_valid(raise_exception=True)
        shipping = shipping_serializer.save()

        order = Order.objects.create(user=user, shipping=shipping)

        item = OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price=product.price
        )
        product.stock -= quantity
        product.save()

        send_order_email.delay(user.email, order.id)
        order.total_price = item.get_total_price() + shipping.cost
        order.save()

        return {
            "order": order,
            "item": item,
            "shipping": shipping
        }


class CheckoutSerializer(serializers.Serializer):
    shipping = ShippingSerializer()

    def validate(self, attrs):
        user = self.context['request'].user
        cart = Cart.objects.prefetch_related('items').filter(user=user).first()

        if not cart or not cart.items.exists():
            raise serializers.ValidationError("Корзина пуста")

        attrs['cart'] = cart
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        cart = validated_data['cart']
        shipping_data = validated_data['shipping']

        shipping_serializer = ShippingSerializer(data=shipping_data)
        shipping_serializer.is_valid(raise_exception=True)
        shipping = shipping_serializer.save()

        order = Order.objects.create(user=user, shipping=shipping)
        total = 0

        for cart_item in cart.items.all():
            product = cart_item.product
            quantity = cart_item.quantity

            if quantity > product.stock:
                raise serializers.ValidationError(
                    f"{product.title}: только {product.stock} шт. в наличии"
                )

            item = OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )

            product.stock -= quantity
            product.save()

            total += item.get_total_price()

        send_order_email.delay(user.email, order.id)
        order.total_price = total + shipping.cost
        order.save()
        cart.items.all().delete()

        return {
            "order": order,
            "shipping": shipping,
            "products_total": total
        }