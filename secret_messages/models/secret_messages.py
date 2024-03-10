from django.db import models
from users.models import User

__all__ = ('SecretMessage',)


class SecretMessage(models.Model):
    id = models.UUIDField(primary_key=True)
    text = models.CharField(max_length=4096)
    sender = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='sent_secret_message',
    )
    recipient = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='received_secret_message',
    )
    deleted_at = models.DateTimeField(null=True, blank=True)
    seen_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_seen(self) -> bool:
        return self.seen_at is not None

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None
