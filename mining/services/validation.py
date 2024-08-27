from datetime import datetime, timedelta

from django.utils import timezone

from mining.exceptions import MiningCooldownError

__all__ = ('validate_mining_time',)


def compute_next_mining_at(
        last_mining_at: datetime,
        is_premium: bool,
) -> datetime:
    if is_premium:
        return last_mining_at + timedelta(hours=1, minutes=30)
    return last_mining_at + timedelta(hours=3)


def validate_mining_time(last_mining_at: datetime, is_premium: bool) -> None:
    next_mining_at = compute_next_mining_at(
        last_mining_at=last_mining_at,
        is_premium=is_premium,
    )

    time_before_next_mining = next_mining_at - timezone.now()

    next_mining_in_seconds = int(time_before_next_mining.total_seconds())
    if next_mining_in_seconds > 0:
        raise MiningCooldownError(next_mining_in_seconds)
