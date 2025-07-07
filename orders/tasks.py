import logging
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)

@shared_task
def send_order_email(email, order_id):
    try:
        send_mail(
            subject='Ваш заказ оформлен',
            message=f'Спасибо за заказ #{order_id}.!!',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False
        )
        logger.info(f"Письмо успешно отправлено на {email}")
    except Exception as e:
        logger.error(f"Ошибка при отправке письма: {e}")

