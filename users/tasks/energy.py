from celery import shared_task
from django.db.models import F

from users.models import User


@shared_task
def decrease_all_energy(energy: int):
    users_with_energy = User.objects.filter(energy__gt=0)
    users_with_energy.update(energy=F('energy') - energy)
