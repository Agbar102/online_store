import logging

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.core.cache import cache

from cart.models import Cart

logger = logging.getLogger(__name__)

@shared_task
def send_cart_remember():
    carts = Cart.objects.prefetch_related('items').select_related('user')

    for cart in carts:
        if not cart.items.exists():
            continue

        cache_key = f"cart_reminder_sent_{cart.id}"
        if cache.get(cache_key):
            continue

        try:
            send_mail(
                subject="Вы забыли оформить заказ",
                message="У вас есть товары в корзине. Завершите покупку прямо сейчас!",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[cart.user.email],
                fail_silently=False
            )
            cache.set(cache_key, True, timeout=60 * 60 * 24)
            logger.info(f"Письмо отправлено на {cart.user.email}")
        except Exception as e:
            logger.error(f"Ошибка при отправке письма: {e}")
