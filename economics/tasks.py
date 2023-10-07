from celery import shared_task

from economics.services import compute_user_balance, tax_user
from users.models import User


@shared_task
def tax_users() -> None:
    users = User.objects.all()

    for user in users:
        user_balance = compute_user_balance(user)

        if user_balance < 50000:
            continue

        tax_user(user=user, balance=user_balance)
