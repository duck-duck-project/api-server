from django.db.models import Sum, Case, When, F, Q

from economics.models import Transaction, UserBalance
from users.models import User

__all__ = ('compute_user_balance', 'sort_richest_users', 'get_user_balances')


def compute_user_balance(user: User) -> int:
    total_amount_sent = Sum(
        Case(
            When(
                sender=user,
                then=F('amount'),
            ),
            default=0,
        )
    )
    total_amount_received = Sum(
        Case(
            When(
                recipient=user,
                then=F('amount'),
            ),
            default=0,
        )
    )
    balance = (
        Transaction
        .objects
        .filter(Q(sender=user) | Q(recipient=user))
        .annotate(
            total_amount_sent=total_amount_sent,
            total_amount_received=total_amount_received,
        )
        .aggregate(
            total_sent=Sum('total_amount_sent'),
            total_received=Sum('total_amount_received'),
        )
    )

    return (balance['total_received'] or 0) - (balance['total_sent'] or 0)


def get_user_balances() -> list[UserBalance]:
    sent_transactions = (
        Transaction
        .objects
        .select_related('sender')
        .exclude(sender__isnull=True)
        .values('sender_id', 'sender__fullname', 'sender__username')
        .annotate(sent_amount=Sum('amount'))
    )
    received_transactions = (
        Transaction
        .objects
        .select_related('recipient')
        .exclude(recipient__isnull=True)
        .values('recipient_id', 'recipient__fullname', 'recipient__username')
        .annotate(received_amount=Sum('amount'))
    )
    sender_id_to_amount = {
        transactions_statistics['sender_id']: transactions_statistics
        for transactions_statistics in sent_transactions
    }
    recipient_id_to_amount = {
        transactions_statistics['recipient_id']: transactions_statistics
        for transactions_statistics in received_transactions
    }
    user_ids = set(sender_id_to_amount) | set(recipient_id_to_amount)

    user_balances: list[UserBalance] = []
    for user_id in user_ids:
        sent_transactions_statistics = sender_id_to_amount.get(user_id)
        received_transactions_statistics = recipient_id_to_amount.get(user_id)

        has_sent_transactions_statistics = (
                sent_transactions_statistics is not None
        )
        has_received_transactions_statistics = (
                received_transactions_statistics is not None
        )
        if (
                has_sent_transactions_statistics
                and has_received_transactions_statistics
        ):
            sent_amount = sent_transactions_statistics['sent_amount']
            received_amount = received_transactions_statistics[
                'received_amount']
            user_username = sent_transactions_statistics['sender__username']
            user_fullname = sent_transactions_statistics['sender__fullname']
            user_balance = received_amount - sent_amount
        elif has_sent_transactions_statistics:
            user_balance = -sent_transactions_statistics['sent_amount']
            user_username = sent_transactions_statistics['sender__username']
            user_fullname = sent_transactions_statistics['sender__fullname']
        elif has_received_transactions_statistics:
            user_balance = received_transactions_statistics['received_amount']
            user_username = received_transactions_statistics['recipient__username']
            user_fullname = received_transactions_statistics['recipient__fullname']
        else:
            continue

        user_balances.append(
            UserBalance(
                user_id=user_id,
                user_fullname=user_fullname,
                user_username=user_username,
                balance=user_balance,
            )
        )

    return user_balances


def sort_richest_users(user_balances: list[UserBalance]) -> list[UserBalance]:
    return sorted(
        user_balances,
        key=lambda user_balance: user_balance.balance,
        reverse=True,
    )
