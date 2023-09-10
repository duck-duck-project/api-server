from django.db.models import Sum

from economics.exceptions import InsufficientFundsForTransferError
from economics.models import Transaction
from users.models import User

__all__ = ('compute_user_balance', 'create_transfer')


def create_transfer(
        *,
        sender: User,
        recipient: User,
        amount: int,
        description: str | None = None,
) -> Transaction:
    """Create a transfer between two users.

    Keyword Args:
        sender: Sender of the transfer.
        recipient: Recipient of the transfer.
        amount: Amount of the transfer.
        description: Description of the transfer.

    Returns:
        The created transfer.
    """
    sender_balance = compute_user_balance(sender)

    if sender_balance < amount:
        raise InsufficientFundsForTransferError(
            sender_id=sender.id,
            sender_balance=sender_balance,
            transfer_amount=amount,
            recipient_id=recipient.id,
        )

    transaction = Transaction(
        sender=sender,
        recipient=recipient,
        amount=amount,
        description=description,
        source=Transaction.Source.TRANSFER,
    )

    transaction.full_clean()
    transaction.save()

    return transaction


def compute_user_balance(user: User) -> int:
    income = (
        Transaction
        .objects
        .filter(recipient=user)
        .aggregate(Sum('amount'))
    )
    spending = (
        Transaction
        .objects
        .filter(sender=user)
        .aggregate(Sum('amount'))
    )
    return (income['amount__sum'] or 0) - (spending['amount__sum'] or 0)
