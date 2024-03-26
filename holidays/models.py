from dataclasses import dataclass

from django.db import models

__all__ = ('Holiday', 'DateHolidays')


@dataclass(frozen=True, slots=True)
class DateHolidays:
    month: int
    day: int
    holidays: list[str]


class Holiday(models.Model):
    name = models.TextField(max_length=1024)
    day = models.PositiveSmallIntegerField()
    month = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('month', 'day', 'name')
