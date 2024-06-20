from dataclasses import dataclass

from django.db import transaction

from user_characteristics.models import SportActivity, SportActivityAction
from user_characteristics.selectors.sport_activity_actions import (
    get_last_sport_activity_action,
)
from user_characteristics.services.sport_activity_actions.validation import (
    validate_sport_activity_action_cooldown,
)
from users.models import User
from users.services.users import decrease_user_energy, increase_user_health

__all__ = ('create_sport_activity_action',)


@dataclass(frozen=True, slots=True)
class SportActivityActionResult:
    user_id: int
    user_energy: int
    user_health: int
    energy_cost_value: int
    sport_activity_name: str
    health_benefit_value: int
    cooldown_in_seconds: int


@transaction.atomic
def create_sport_activity_action(
        *,
        user: User,
        sport_activity: SportActivity,
) -> SportActivityActionResult:
    last_sport_activity_action = get_last_sport_activity_action(user)

    if last_sport_activity_action is not None:
        validate_sport_activity_action_cooldown(last_sport_activity_action)

    user = decrease_user_energy(
        user=user,
        decrease=sport_activity.energy_cost_value,
    )
    user = increase_user_health(
        user=user,
        increase=sport_activity.health_benefit_value,
    )

    SportActivityAction.objects.create(
        user=user,
        sport_activity=sport_activity,
    )
    return SportActivityActionResult(
        user_id=user.id,
        user_energy=user.energy,
        user_health=user.health,
        energy_cost_value=sport_activity.energy_cost_value,
        sport_activity_name=sport_activity.name,
        health_benefit_value=sport_activity.health_benefit_value,
        cooldown_in_seconds=sport_activity.cooldown_in_seconds,
    )
