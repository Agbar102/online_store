# import logging
# from django.db.models.signals import pre_save
# from django.dispatch import receiver
# from .models import Order
# from .tasks import send_order_status_email
#
# logger = logging.getLogger(__name__)
#
#
# @receiver(pre_save, sender=Order)
# def order_status_updated(sender, instance, **kwargs):
#     if not instance.pk:
#         return
#     try:
#         old_order = Order.objects.get(pk=instance.pk)
#     except Order.DoesNotExist:
#         return
#
#     if old_order.status != instance.status:
#         logger.info(f"Статус заказа #{instance.id} изменён: {old_order.get_status_display()} → {instance.get_status_display()}")
#         send_order_status_email.delay(instance.user.email, instance.id, instance.get_status_display())
