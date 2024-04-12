from django.db import models

from users.models.users import User

__all__ = ('Tag',)


class Tag(models.Model):
    class Weight(models.IntegerChoices):
        GOLD = 1
        SILVER = 2
        BRONZE = 3

    of_user = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='given_tag',
    )
    to_user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='received_tag',
    )
    text = models.CharField(max_length=32)
    weight = models.PositiveSmallIntegerField(choices=Weight.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.text)
