from uuid import uuid4

from django.db import models

from users.models import User

__all__ = ('Contact', 'SecretMessage', 'SecretMedia')


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

    class Meta:
        unique_together = ('of_user', 'to_user')


class SecretMessage(models.Model):
    id = models.UUIDField(primary_key=True)
    text = models.CharField(max_length=200)


class SecretMedia(models.Model):

    class MediaType(models.IntegerChoices):
        PHOTO = 1
        VOICE = 2

    id = models.UUIDField(primary_key=True, default=uuid4)
    name = models.CharField(max_length=64, null=True, blank=True)
    contact = models.ForeignKey(
        to=Contact,
        on_delete=models.SET_NULL,
        null=True,
    )
    file_id = models.CharField(max_length=255, unique=True)
    media_type = models.PositiveSmallIntegerField(choices=MediaType.choices)
