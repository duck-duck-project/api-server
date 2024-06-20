from user_characteristics.models import SportActivity
from user_characteristics.models.sport_activity_actions import (
    SportActivityAction,
)
from user_characteristics.selectors.sport_activity_actions import \
    get_last_sport_activity_action
from users.models import User


__all__ = ('create_sport_activity_action',)


def compute_time_before_next_sport_activity_in_seconds() -> int:
    pass


def validate_sport_activity_action_cooldown(
        
) -> None:
    pass


def create_sport_activity_action(
        *,
        user: User,
        sport_activity: SportActivity,
) -> SportActivityAction:
    last_sport_activity = get_last_sport_activity_action(user)

    return SportActivityAction.objects.create()


