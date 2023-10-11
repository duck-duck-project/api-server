from dataclasses import dataclass
from datetime import date
from typing import NewType

__all__ = ('HTML', 'DailyFoodMenu', 'FoodMenuItem')

HTML = NewType('HTML', str)


@dataclass(frozen=True, slots=True)
class FoodMenuItem:
    name: str
    calories_count: int
    photo_url: str


@dataclass(frozen=True, slots=True)
class DailyFoodMenu:
    items: list[FoodMenuItem]
    at: date
