from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_message_register(email, code):
    send_mail(
        subject='Код подтверждения',
        message=f'Ваш код подтверждения: {code}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email,],
        fail_silently=False
    )


