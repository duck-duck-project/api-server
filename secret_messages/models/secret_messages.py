from django.db import models

__all__ = ('SecretMessage',)


class SecretMessage(models.Model):
    id = models.UUIDField(primary_key=True)
    text = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
