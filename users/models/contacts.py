from django.db import models

from users.models.themes import Theme
from users.models.users import User

__all__ = ('Contact',)


class Contact(models.Model):
    of_user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='of_user',
    )
    to_user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='to_user',
    )
    private_name = models.CharField(max_length=32)
    public_name = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    is_hidden = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    theme = models.ForeignKey(
        to=Theme,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        unique_together = ('of_user', 'to_user')

    def __str__(self):
        return self.public_name
