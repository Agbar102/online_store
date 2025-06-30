from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_order_email(email, order_id):
    send_mail(
        subject='Ваш заказ оформлен',
        message=f'Спасибо за заказ #{order_id}.!!',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently = False
    )