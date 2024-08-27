from django.db import models

from users.models import Contact

__all__ = ('SecretTextMessage',)


class SecretTextMessage(models.Model):
    id = models.UUIDField(primary_key=True)
    text = models.CharField(max_length=200)
    contact = models.ForeignKey(
        to=Contact,
        on_delete=models.CASCADE,
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
