from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


@shared_task
def send_message_register(email, code):
    send_mail(
        subject='Код подтверждения',
        message=f'Ваш код подтверждения: {code}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email,],
        fail_silently=False
    )


@shared_task()
def delete_not_active_users():
    ten_minutes = timezone.now() - timedelta(minutes=10)
    User.objects.filter(is_active=False, confirmation_send__lt=ten_minutes).delete()
