from django.db import models

from secret_messages.models.secret_message_templates import (
    SecretMessageTemplate,
)

__all__ = ('User',)


class User(models.Model):
    fullname = models.CharField(max_length=64)
    username = models.CharField(max_length=64, null=True, blank=True)
    is_premium = models.BooleanField(default=False)
    can_be_added_to_contacts = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    secret_message_template = models.ForeignKey(
        to=SecretMessageTemplate,
        on_delete=models.SET_NULL,
        null=True,
    )
