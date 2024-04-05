from django.db import models

__all__ = ('Nationality',)


class Nationality(models.Model):
    name = models.CharField(max_length=64, unique=True)

    class Meta:
        verbose_name_plural = 'nationalities'

    def __str__(self):
        return self.name
