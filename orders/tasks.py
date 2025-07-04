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


@shared_task
def send_order_status_email(email, order_id, status_display):
    logger.info(f"Отправка email пользователю {email} по заказу #{order_id} со статусом '{status_display}'")
    try:
        send_mail(
            subject=f"Статус заказа #{order_id} обновлён",
            message=f"Ваш заказ #{order_id} теперь имеет статус: {status_display}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False
        )
        logger.info(f"Успешно отправлено email на {email}")
    except Exception as e:
        logger.error(f"Ошибка при отправке email на {email}: {str(e)}")