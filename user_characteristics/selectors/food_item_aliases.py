from django.db.models import QuerySet

from user_characteristics.models import FoodItemAlias

__all__ = ('get_food_item_alias_by_name',)


def get_food_item_alias_by_name(name: str) -> FoodItemAlias | None:
    # All aliases are stored in lowercase in database
    name = name.lower()
    return (
        FoodItemAlias.objects
        .select_related('food_item')
        .filter(name=name)
        .first()
    )
