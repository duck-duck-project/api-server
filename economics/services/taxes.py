from economics.models import Transaction
from economics.services.withdrawal import create_system_withdrawal
from users.models import User

__all__ = ('tax_user',)


def tax_user(*, user: User, balance: int) -> Transaction:
    amount_to_withdraw_as_tax = int(balance * 0.1)
    return create_system_withdrawal(
        user=user,
        amount=amount_to_withdraw_as_tax,
        description='Налог на имущество',
    )
