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

__all__ = ('feed_user', 'UserFeedResult')


@dataclass(frozen=True, slots=True)
class UserFeedResult:
    from_user_id: int
    to_user_id: int
    food_item_name: str
    food_item_emoji: str | None
    price: int
    energy_benefit_value: int
    health_impact_value: int
    user_energy: int
    user_health: int


@transaction.atomic
def feed_user(
        *,
        from_user: User,
        to_user: User,
        food_item: FoodItem,
) -> UserFeedResult:
    """
    Feed user with food item.

    Keyword Args:
        from_user: User who is buying food item.
        to_user: User who is consuming food item.
        food_item: Food item to consume.

    Raises:
        InsufficientFundsForSystemWithdrawalError:
            If user does not have enough balance.
        NotEnoughHealthError:
            If user does not have enough health to consume food item.

    Returns:
        UserFeedResult: Result of feeding user with food item.
    """
    create_system_withdrawal(
        user=from_user,
        amount=food_item.price,
        description=f'Покупка еды {food_item.name} для {to_user.fullname}'
    )
    user = increase_user_energy(
        user=to_user,
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

    return UserFeedResult(
        from_user_id=from_user.id,
        to_user_id=to_user.id,
        food_item_name=food_item.name,
        food_item_emoji=food_item.emoji,
        price=food_item.price,
        energy_benefit_value=food_item.energy_benefit_value,
        health_impact_value=food_item.health_impact_value,
        user_energy=user.energy,
        user_health=user.health,
    )
