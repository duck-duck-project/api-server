from uuid import UUID

from django.db.models import QuerySet, Q

from economics.exceptions import TransactionDoesNotExistError
from economics.models import Transaction

__all__ = ('get_latest_user_transactions', 'get_transaction_by_id')


def filter_user_transactions(
        *,
        transactions: QuerySet[Transaction],
        user_id: int,
) -> QuerySet[Transaction]:
    return transactions.filter(Q(sender_id=user_id) | Q(recipient_id=user_id))


def get_latest_user_transactions(
        *,
        user_id: int,
        limit: int,
        offset: int,
) -> QuerySet[Transaction]:
    transactions = Transaction.objects.select_related('sender', 'recipient')
    transactions_of_user = filter_user_transactions(
        transactions=transactions,
        user_id=user_id,
    )
    latest_transactions = (
        transactions_of_user.order_by('-created_at')[offset:offset + limit]
    )
    return latest_transactions.only(
        'id',
        'sender__id',
        'sender__username',
        'sender__fullname',
        'recipient__id',
        'recipient__username',
        'recipient__fullname',
        'amount',
        'description',
        'created_at',
    )


def get_transaction_by_id(transaction_id: UUID) -> Transaction:
    """
    Get transaction by id.

    Args:
        transaction_id: Transaction id.

    Raises:
        TransactionDoesNotExistError: If transaction with given id
                                      does not exist.
    """
    try:
        return (
            Transaction.objects
            .select_related('sender')
            .get(id=transaction_id)
        )
    except Transaction.DoesNotExist:
        raise TransactionDoesNotExistError(
            f'Transaction with id {transaction_id} does not exist',
        )
