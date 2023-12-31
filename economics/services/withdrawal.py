from economics.exceptions import InsufficientFundsForSystemWithdrawalError
from economics.models import Transaction
from economics.services.balance import compute_user_balance
from users.models import User

__all__ = ('create_system_withdrawal',)


def create_system_withdrawal(
        *,
        user: User,
        amount: int,
        description: str | None = None,
) -> Transaction:
    """Create a system withdrawal for a user.

    Keyword Args:
        user: Sender of the withdrawal.
        amount: Amount of the withdrawal.
        description: Description of the withdrawal.

    Returns:
        The created withdrawal.
    """
    balance = compute_user_balance(user)

    if balance < amount:
        raise InsufficientFundsForSystemWithdrawalError(
            user_id=user.id,
            balance=balance,
            amount=amount,
            description=description,
        )

    transaction = Transaction(
        sender=user,
        amount=amount,
        description=description,
    )

    transaction.full_clean()
    transaction.save()

    return transaction
