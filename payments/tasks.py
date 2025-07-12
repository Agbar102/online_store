from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_payment_success_email(email, order_id, total_price):
    subject = f"Ваш заказ №{order_id} успешно оплачен"
    message = f"Здравствуйте, \n\nВаш заказ на сумму {total_price} был успешно оплачен."
    send_mail(subject, message, from_email=settings.EMAIL_HOST_USER, recipient_list=[email],
            fail_silently=False)