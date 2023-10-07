from economics.models import Transaction
from economics.services import create_system_deposit
from users.models import User

__all__ = ('tax_user',)


def tax_user(*, user: User, balance: int) -> Transaction:
    amount_to_withdraw_as_tax = int(balance * 0.1)
    return create_system_deposit(
        user=user,
        amount=amount_to_withdraw_as_tax,
        description='Tax',
    )
