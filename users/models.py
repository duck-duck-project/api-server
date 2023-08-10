from django.db import models

from secret_messages.models.secret_message_templates import (
    SecretMessageButtonTemplate,
    SecretMessageDescriptionTemplate,
)

__all__ = ('User', 'Preferences', 'Contact')


class User(models.Model):
    """User model."""
    fullname = models.CharField(max_length=64)
    username = models.CharField(max_length=64, null=True, blank=True)
    is_premium = models.BooleanField(default=False)
    can_be_added_to_contacts = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Contact(models.Model):
    """User contacts."""
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


class Preferences(models.Model):
    """User preferences."""
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
