from typing import TypedDict

from user_characteristics.exceptions import FoodItemNotFoundError
from user_characteristics.models import FoodItem
from user_characteristics.selectors.food_item_aliases import (
    get_food_item_alias_by_name,
)

__all__ = (
    'FoodItemTypedDict',
    'get_food_items',
    'get_food_item_by_name_and_type',
)


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


def get_food_item_by_name_and_type(
        food_item_name: str,
        food_item_type: int,
) -> FoodItem:
    alias = get_food_item_alias_by_name(food_item_name)
    if alias is not None and alias.food_item.type == food_item_type:
        return alias.food_item

    try:
        return FoodItem.objects.get(
            name__iexact=food_item_name,
            type=food_item_type,
        )
    except FoodItem.DoesNotExist:
        raise FoodItemNotFoundError(
            food_item_name=food_item_name,
            food_item_type=food_item_type,
        )
