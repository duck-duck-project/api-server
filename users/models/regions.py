from django.db import models

from users.models.countries import Country

__all__ = ('Region',)


class Region(models.Model):
    name = models.CharField(max_length=64, unique=True)
    country = models.ForeignKey(to=Country, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.country} | {self.name}'
