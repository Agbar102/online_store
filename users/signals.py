from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from .models import UserActivity, CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()


@receiver(post_save, sender=User)
def log_user_register(sender, instance, created, **kwargs):
    if created:
        UserActivity.objects.create(
            user=instance,
            method='REGISTER',
            path='/register/',
            time_start=now(),
            data="Пользователь зарегестрирован"
        )
