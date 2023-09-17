from django.db.models import Sum, Case, When, F, Q

from economics.models import Transaction
from users.models import User

__all__ = ('compute_user_balance',)


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
