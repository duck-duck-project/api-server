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
        .exclude(sender__isnull=True)
        .values('sender_id')
        .annotate(sent_amount=Sum('amount'))
    )
    received_transactions = (
        Transaction
        .objects
        .exclude(recipient__isnull=True)
        .values('recipient_id')
        .annotate(received_amount=Sum('amount'))
    )
    sender_id_to_amount = {
        user['sender_id']: user['sent_amount']
        for user in sent_transactions
    }
    recipient_id_to_amount = {
        user['recipient_id']: user['received_amount']
        for user in received_transactions
    }
    user_ids = set(sender_id_to_amount) | set(recipient_id_to_amount)

    user_balances: list[UserBalance] = []
    for user_id in user_ids:
        sent_amount = sender_id_to_amount.get(user_id, 0)
        received_amount = recipient_id_to_amount.get(user_id, 0)

        user_balance = received_amount - sent_amount

        user_balances.append(
            UserBalance(
                user_id=user_id,
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
