from economics.exceptions import (
    InsufficientFundsForTransferError,
    TransferSenderDoesNotMatchError,
    TransactionIsNotTransferError,
)
from economics.models import Transaction
from economics.services.balance import compute_user_balance
from users.models import User

__all__ = ('create_transfer', 'delete_user_transaction')


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
    )

    transaction.full_clean()
    transaction.save()

    return transaction


def delete_user_transaction(
        *,
        transaction: Transaction,
        user_id: int,
) -> None:
    """Delete a user's transaction.

    Keyword Args:
        transaction: Transaction to delete.
        user_id: ID of the user who owns the transaction.

    Raises:
        TransactionIsNotTransferError: If the transaction is not a transfer.
        TransferSenderDoesNotMatchError: If the transaction's sender does not
                                         match the user.
    """
    if not transaction.is_transfer:
        raise TransactionIsNotTransferError(
            transaction_id=transaction.id,
        )
    if transaction.sender_id != user_id:
        raise TransferSenderDoesNotMatchError(
            transaction_id=transaction.id,
            sender_id=transaction.sender_id,
        )
    transaction.delete()
