from django.db import models

from users.models import User

__all__ = ('Contact', 'SecretMessage')


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


class SecretMessage(models.Model):
    contact = models.ForeignKey(
        to=Contact,
        on_delete=models.SET_NULL,
        null=True,
    )
    text = models.CharField(max_length=200)
