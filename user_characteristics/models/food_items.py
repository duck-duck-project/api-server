from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models.users import USER_MAX_ENERGY, USER_MAX_HEALTH

__all__ = ('FoodItem',)


class FoodItem(models.Model):
    class Type(models.IntegerChoices):
        FOOD = 1
        DRINK = 2

    name = models.CharField(max_length=64, unique=True)
    emoji = models.CharField(max_length=16, blank=True, null=True)
    type = models.PositiveSmallIntegerField(choices=Type.choices)
    price = models.PositiveIntegerField(
        validators=(MinValueValidator(1),)
    )
    energy_benefit_value = models.PositiveSmallIntegerField(
        validators=(
            MinValueValidator(1),
            MaxValueValidator(USER_MAX_ENERGY),
        )
    )
    health_impact_value = models.SmallIntegerField(
        validators=(
            MinValueValidator(-USER_MAX_HEALTH),
            MaxValueValidator(USER_MAX_HEALTH),
        )
    )

    def __str__(self) -> str:
        if self.emoji is not None:
            return f'{self.emoji} {self.name}'
        return self.name
