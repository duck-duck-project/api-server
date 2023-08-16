from django.db import models

from secret_messages.models.secret_message_themes import SecretMessageTheme

__all__ = ('User', 'Contact')


class User(models.Model):
    """User model."""
    fullname = models.CharField(max_length=64)
    username = models.CharField(max_length=64, null=True, blank=True)
    is_premium = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    secret_message_theme = models.ForeignKey(
        to=SecretMessageTheme,
        on_delete=models.SET_NULL,
        null=True,
    )
    can_be_added_to_contacts = models.BooleanField(default=True)

    def __str__(self):
        return self.username or self.fullname


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
    profile_photo_url = models.URLField(null=True, blank=True)

    class Meta:
        unique_together = ('of_user', 'to_user')
