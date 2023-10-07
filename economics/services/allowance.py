from economics.models import Transaction
from economics.services.deposit import create_system_deposit
from users.models import User

__all__ = ('create_allowance',)


def compute_allowance_amount(balance: int) -> int:
    return int((1000 - balance) * 0.1)


def create_allowance(*, user: User, balance: int) -> Transaction:
    return create_system_deposit(
        user=user,
        amount=compute_allowance_amount(balance),
        description='Пособие по безработице',
    )
