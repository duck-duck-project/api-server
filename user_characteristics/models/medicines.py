from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import USER_MAX_HEALTH

__all__ = ('Medicine',)


class Medicine(models.Model):
    name = models.CharField(max_length=64, unique=True)
    emoji = models.CharField(max_length=16, blank=True, null=True)
    health_benefit_value = models.PositiveSmallIntegerField(
        validators=(
            MinValueValidator(1),
            MaxValueValidator(USER_MAX_HEALTH),
        )
    )
    price = models.PositiveIntegerField(
        validators=(MinValueValidator(1),)
    )

    def __str__(self) -> str:
        if self.emoji is not None:
            return f'{self.emoji} {self.name}'
        return self.name
