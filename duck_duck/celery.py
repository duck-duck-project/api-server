import os

from celery import Celery

__all__ = ('app',)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'duck_duck.settings')

app = Celery('duck_duck')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
