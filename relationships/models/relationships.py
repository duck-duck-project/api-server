import math

from django.db import models

from users.models import User

__all__ = ('Relationship',)


class Relationship(models.Model):
    first_user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='first_user_set',
    )
    second_user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='second_user_set',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    broke_up_at = models.DateTimeField(null=True, blank=True)
    experience = models.PositiveBigIntegerField(default=0)

    @property
    def level(self) -> int:
        # log2 of 0 is undefined, so we need to handle
        # that case separately
        if self.experience == 0:
            return 0
        return int(math.log2(self.experience))

    @property
    def next_level(self) -> int:
        return self.level + 1

    @property
    def next_level_experience_threshold(self) -> int:
        return 2 ** self.next_level

    @property
    def experience_to_next_level(self) -> int:
        return self.next_level_experience_threshold - self.experience
