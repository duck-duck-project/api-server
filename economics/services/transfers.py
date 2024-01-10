from django.utils import timezone

from economics.exceptions import (
    InsufficientFundsForTransferError,
    TransferSenderDoesNotMatchError,
    TransactionIsNotTransferError,
    TransferRollbackTimeExpiredError,
    InsufficientFundsForTransferRollbackError,
)
from economics.models import Transaction
from economics.services.balance import compute_user_balance
from users.models import User

__all__ = ('create_transfer', 'rollback_transfer')


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


def validate_transaction_is_transfer(transaction: Transaction) -> None:
    if not transaction.is_transfer:
        raise TransactionIsNotTransferError('Transaction is not a transfer')


def validate_transfer_sender_matches_user(
        *,
        transaction: Transaction,
        user_id: int,
) -> None:
    if transaction.sender_id != user_id:
        raise TransferSenderDoesNotMatchError(
            'Transaction does not belong to user',
        )


def validate_transfer_rollback_time_expired(transaction: Transaction) -> None:
    now = timezone.now()
    is_transfer_rollback_time_expired = (
            now - transaction.created_at > timezone.timedelta(minutes=10)
    )
    if is_transfer_rollback_time_expired:
        raise TransferRollbackTimeExpiredError(
            'Transfer rollback time expired',
        )


def validate_user_balance_for_transfer_rollback(
        transaction: Transaction,
) -> None:
    user_balance = compute_user_balance(user=transaction.sender)
    if user_balance < transaction.amount:
        raise InsufficientFundsForTransferRollbackError(
            'Insufficient funds for transfer rollback'
        )


def rollback_transfer(*, transaction: Transaction, user_id: int) -> None:
    """Delete a user's transaction.

    Keyword Args:
        transaction: Transaction to delete.
        user_id: ID of the user who is deleting the transaction.

    Raises:
        TransactionIsNotTransferError: If the transaction is not a transfer.
        TransferSenderDoesNotMatchError: If the transaction's sender does not
                                         match the user.
        TransferRollbackTimeExpiredError: If the transaction rollback time
                                          expired.
        InsufficientFundsForTransferRollbackError: If the user has insufficient
                                                  funds to rollback the
                                                  transfer.
    """
    validate_transaction_is_transfer(transaction)
    validate_transfer_sender_matches_user(
        transaction=transaction,
        user_id=user_id,
    )
    validate_transfer_rollback_time_expired(transaction)
    validate_user_balance_for_transfer_rollback(transaction)

    transaction.delete()
