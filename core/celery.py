import os
from celery.schedules import crontab
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'lonely_task': {
        'task': 'cart.tasks.send_cart_remember',
        'schedule': crontab(minute=0, hour=21),
    },
}

app.conf.beat_schedule = {
    'delete_not_active_users_every_10_minutes': {
        'task': 'users.tasks.delete_not_active_users',
        'schedule': crontab(minute='*/10'),
    },
}