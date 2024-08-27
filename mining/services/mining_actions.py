from dataclasses import dataclass

from django.db import transaction

from economics.services import create_system_deposit
from mining.models import MiningAction
from mining.selectors import get_last_mining_action
from mining.services.domain import (
    get_energy_cost, get_health_cost, get_random_mined_resource,
)
from mining.services.validation import validate_mining_time
from users.models import User
from users.services.users import decrease_user_energy, decrease_user_health

__all__ = ('create_mining_action',)


@dataclass(frozen=True, slots=True)
class MiningActionResult:
    user_id: int
    chat_id: int | None
    resource_name: str
    value_per_gram: int
    weight_in_grams: int
    value: int
    spent_energy: int
    remaining_energy: int
    spent_health: int
    remaining_health: int


@transaction.atomic
def create_mining_action(
        *,
        user: User,
        chat_id: int | None,
) -> MiningActionResult:
    mined_resource = get_random_mined_resource(user.is_premium)

    last_mining_action = get_last_mining_action(user_id=user.id)

    if last_mining_action is not None:
        validate_mining_time(
            last_mining_at=last_mining_action.created_at,
            is_premium=user.is_premium,
        )

    energy_cost = get_energy_cost(user.is_premium)
    health_cost = get_health_cost(user.is_premium)

    decrease_user_energy(user, energy_cost)
    decrease_user_health(user, health_cost)
    mining_action = MiningAction.objects.create(
        user_id=user.id,
        resource_name=mined_resource.name,
        value=mined_resource.value,
        chat_id=chat_id,
    )
    create_system_deposit(
        user=user,
        description=f'⛏️ Работа на шахте ({mining_action.resource_name})',
        amount=mining_action.value,
    )
    return MiningActionResult(
        user_id=user.id,
        chat_id=chat_id,
        resource_name=mined_resource.name,
        value=mined_resource.value,
        spent_energy=energy_cost,
        remaining_energy=user.energy,
        weight_in_grams=mined_resource.weight_in_grams,
        value_per_gram=mined_resource.value_per_gram,
        spent_health=health_cost,
        remaining_health=user.health,
    )
