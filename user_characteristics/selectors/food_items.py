from typing import TypedDict

from user_characteristics.exceptions import FoodItemDoesNotExistError
from user_characteristics.models import FoodItem

__all__ = ('FoodItemTypedDict', 'get_food_items', 'get_food_item_by_name')


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


def get_food_item_by_name(food_item_name: str) -> FoodItem:
    try:
        return FoodItem.objects.get(name=food_item_name)
    except FoodItem.DoesNotExist:
        raise FoodItemDoesNotExistError(food_item_name)
