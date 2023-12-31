from economics.models import Transaction
from users.models import User

__all__ = ('create_system_deposit',)


def create_system_deposit(
        *,
        user: User,
        amount: int,
        description: str | None = None,
) -> Transaction:
    """Create a system deposit for a user.

    Keyword Args:
        user: Recipient of the deposit.
        amount: Amount of the deposit.
        description: Description of the deposit.

    Returns:
        The created deposit.
    """
    transaction = Transaction(
        recipient=user,
        amount=amount,
        description=description,
    )

    transaction.full_clean()
    transaction.save()

    return transaction
