from typing import TypedDict

from user_characteristics.models import FoodItem

__all__ = ('FoodItemTypedDict', 'get_food_items')


class FoodItemTypedDict(TypedDict):
    name: str
    emoji: str | None
    type: int
    price: int
    energy_benefit_value: int
    health_impact_value: int


def get_food_items() -> tuple[FoodItemTypedDict, ...]:
    return tuple(
        FoodItem.objects
        .values(
            'name',
            'emoji',
            'type',
            'price',
            'energy_benefit_value',
            'health_impact_value',
        )
    )
