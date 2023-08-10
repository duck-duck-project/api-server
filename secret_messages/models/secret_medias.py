from uuid import uuid4

from django.db import models

from users.models import Contact

__all__ = ('SecretMedia',)


class SecretMedia(models.Model):

    class MediaType(models.IntegerChoices):
        PHOTO = 1
        VOICE = 2
        VIDEO = 3
        AUDIO = 4
        ANIMATION = 5
        DOCUMENT = 6
        VIDEO_NOTE = 7
        STICKER = 8

    id = models.UUIDField(primary_key=True, default=uuid4)
    name = models.CharField(max_length=64, null=True, blank=True)
    contact = models.ForeignKey(
        to=Contact,
        on_delete=models.SET_NULL,
        null=True,
    )
    file_id = models.CharField(max_length=255, unique=True)
    media_type = models.PositiveSmallIntegerField(choices=MediaType.choices)
    created_at = models.DateTimeField(auto_now_add=True)
