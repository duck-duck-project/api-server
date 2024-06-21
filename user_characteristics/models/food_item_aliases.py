from django.db import models

from user_characteristics.models.food_items import FoodItem

__all__ = ('FoodItemAlias',)


class FoodItemAlias(models.Model):
    name = models.CharField(max_length=64, unique=True)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'food item alias'
        verbose_name_plural = 'food item aliases'

    def __str__(self):
        return self.name

    def full_clean(
            self,
            exclude=None,
            validate_unique=True,
            validate_constraints=True,
    ):
        self.name = self.name.lower()
        super().full_clean(exclude, validate_unique, validate_constraints)
