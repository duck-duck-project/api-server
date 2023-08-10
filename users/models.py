from django.db import models

from secret_messages.models.secret_message_templates import (
    SecretMessageButtonTemplate,
    SecretMessageDescriptionTemplate,
)

__all__ = ('User', 'Preferences')


class User(models.Model):
    fullname = models.CharField(max_length=64)
    username = models.CharField(max_length=64, null=True, blank=True)
    is_premium = models.BooleanField(default=False)
    can_be_added_to_contacts = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Preferences(models.Model):
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    secret_message_description_template = models.ForeignKey(
        to=SecretMessageDescriptionTemplate,
        on_delete=models.SET_NULL,
        null=True,
    )
    secret_message_description_emoji = models.CharField(
        max_length=16,
        default='📩',
    )
    secret_message_button_template = models.ForeignKey(
        to=SecretMessageButtonTemplate,
        on_delete=models.SET_NULL,
        null=True,
    )
    secret_message_button_emoji = models.CharField(
        max_length=16,
        default='👀',
    )
