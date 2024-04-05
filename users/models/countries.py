from django.db import models

__all__ = ('Country',)


class Country(models.Model):
    name = models.CharField(max_length=64, unique=True)
    flag_emoji = models.CharField(max_length=8)

    class Meta:
        verbose_name_plural = 'countries'

    def __str__(self):
        return f'{self.flag_emoji} {self.name}'
