from economics.exceptions import InsufficientFundsForTransferError
from economics.models import Transaction
from economics.services.balance import compute_user_balance
from users.models import User

__all__ = ('create_transfer',)


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
