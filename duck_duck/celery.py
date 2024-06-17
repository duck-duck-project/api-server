import os

from celery import Celery
from celery.schedules import crontab

__all__ = ('app',)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'duck_duck.settings')

app = Celery('duck_duck')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.beat_schedule = {
    'decrease-all-energy': {
        'task': 'users.tasks.energy.decrease_all_energy',
        'schedule': crontab(hour='1'),
        'args': (60,)
    },
}
