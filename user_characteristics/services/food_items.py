from dataclasses import dataclass

from django.db import transaction

from economics.services import create_system_withdrawal
from user_characteristics.models import FoodItem
from users.models import User
from users.services.users import (
    decrease_user_health,
    increase_user_energy,
    increase_user_health,
)

__all__ = ('consume_food_item',)


@dataclass(frozen=True, slots=True)
class FoodItemConsumptionResult:
    user_id: int
    food_item_name: str
    food_item_emoji: str | None
    price: int
    energy_benefit_value: int
    user_energy: int
    health_impact_value: int
    user_health: int


@transaction.atomic
def consume_food_item(
        *,
        user: User,
        food_item: FoodItem,
) -> FoodItemConsumptionResult:
    create_system_withdrawal(
        user=user,
        amount=food_item.price,
        description=f'Покупка еды {food_item.name}'
    )
    user = increase_user_energy(
        user=user,
        increase=food_item.energy_benefit_value,
    )

    if food_item.health_impact_value > 0:
        user = increase_user_health(
            user=user,
            increase=food_item.health_impact_value,
        )
    elif food_item.health_impact_value < 0:
        user = decrease_user_health(
            user=user,
            decrease=abs(food_item.health_impact_value),
        )

    return FoodItemConsumptionResult(
        user_id=user.id,
        food_item_name=food_item.name,
        food_item_emoji=food_item.emoji,
        price=food_item.price,
        energy_benefit_value=food_item.energy_benefit_value,
        user_energy=user.energy,
        health_impact_value=food_item.health_impact_value,
        user_health=user.health,
    )
