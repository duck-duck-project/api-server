from datetime import datetime, timedelta

from django.utils import timezone

from user_characteristics.exceptions import SportActivityCooldownError
from user_characteristics.models import SportActivityAction

__all__ = (
    'compute_next_sport_activity_time',
    'validate_sport_activity_action_cooldown',
)


def compute_next_sport_activity_time(
        last_activity_time: datetime,
        cooldown_in_seconds: int,
) -> datetime:
    return last_activity_time + timedelta(seconds=cooldown_in_seconds)


def validate_sport_activity_action_cooldown(
        last_sport_activity_action: SportActivityAction,
) -> None:
    sport_activity = last_sport_activity_action.sport_activity
    next_sport_activity_time = compute_next_sport_activity_time(
        last_activity_time=last_sport_activity_action.created_at,
        cooldown_in_seconds=sport_activity.cooldown_in_seconds,
    )
    now = timezone.now()
    if next_sport_activity_time > now:
        next_activity_time = next_sport_activity_time - now

        raise SportActivityCooldownError(
            cooldown_in_seconds=sport_activity.cooldown_in_seconds,
            next_activity_in_seconds=int(next_activity_time.total_seconds()),
        )
