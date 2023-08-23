from django.db import models
from django.utils import timezone

from secret_messages.models.secret_message_themes import SecretMessageTheme

__all__ = ('User', 'Contact', 'Team', 'TeamMember')


class User(models.Model):
    """User model."""
    fullname = models.CharField(max_length=64)
    username = models.CharField(max_length=64, null=True, blank=True)
    subscription_started_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    secret_message_theme = models.ForeignKey(
        to=SecretMessageTheme,
        on_delete=models.SET_NULL,
        null=True,
    )
    can_be_added_to_contacts = models.BooleanField(default=True)
    profile_photo_url = models.URLField(null=True, blank=True)
    is_banned = models.BooleanField(default=False)
    can_receive_notifications = models.BooleanField(default=True)

    def __str__(self):
        return self.username or self.fullname

    @property
    def is_premium(self) -> bool:
        """Determine whether user is premium or not via on subscription date."""
        if self.subscription_started_at is None:
            return False
        return (timezone.now() - self.subscription_started_at).days <= 30


class Team(models.Model):
    name = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class TeamMember(models.Model):
    class Status(models.IntegerChoices):
        MEMBER = 1
        OWNER = 2

    team = models.ForeignKey(to=Team, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(choices=Status.choices)
    is_hidden = models.BooleanField(default=False)
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
    is_deleted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('of_user', 'to_user')

    def __str__(self):
        return self.public_name
