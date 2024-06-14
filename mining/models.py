from datetime import datetime, timedelta

from django.db import models

from users.models import User

__all__ = ('MiningAction',)


class MiningAction(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
    )
    resource_name = models.CharField(max_length=64)
    wealth = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def next_mining_at(self) -> datetime:
        return self.created_at + timedelta(hours=4)
