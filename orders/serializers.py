import logging
from rest_framework import serializers
from .models import OrderItem, Order, Items
from .tasks import send_order_status_email

logger = logging.getLogger(__name__)

class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Items.objects.all())
    product_title = serializers.CharField(source='product.title', read_only=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_title', 'quantity', 'price']



class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'created_at', 'status', 'total_price', 'items']
        read_only_fields = ['created_at', 'total_price']

    def validate(self, attrs):
        items_data = self.initial_data.get('items', [])
        if not items_data:
            raise serializers.ValidationError("Нельзя оформить пустой заказ.")
        for item in items_data:
            if item.get('quantity', 0) < 1:
                raise serializers.ValidationError("Количество товара должно быть больше 0.")
        return attrs

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user
        order = Order.objects.create(user=user, **validated_data)

        total = 0
        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            price = product.price

            order_item = OrderItem.objects.create(
                order=order, product=product, quantity=quantity, price=price
            )
            total += order_item.get_total_price()

        order.total_price = total
        order.save()
        logger.info(f"Создан заказ #{order.id} для пользователя {user}")

        return order

    def update(self, instance, validated_data):
        old_status = instance.status
        instance.status = validated_data.get('status', instance.status)
        instance.save()

        if old_status != instance.status:
            status_display = instance.get_status_display()
            logger.info(f"Смена статуса заказа #{instance.id}: {old_status} -> {instance.status}")
            send_order_status_email.delay(
                instance.user.email,
                instance.id,
                status_display
            )

        instance.items.all().delete()
        items_data = self.initial_data.get('items', [])
        total = 0
        for item_data in items_data:
            product_id = item_data['product']
            try:
                product = Items.objects.get(id=product_id)
            except Items.DoesNotExist:
                raise serializers.ValidationError(f"Продукт с id={product_id} не найден.")
            quantity = item_data['quantity']
            price = product.price

            order_item = OrderItem.objects.create(
                order=instance, product=product, quantity=quantity, price=price
            )
            total += order_item.get_total_price()

        instance.total_price = total
        instance.save()
        logger.info(f"Обновлён заказ #{instance.id}, новая сумма: {total}")
        return instance