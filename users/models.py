from uuid import uuid4

from django.db import models

__all__ = ('User', 'Contact', 'Theme')


class Theme(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    is_hidden = models.BooleanField(default=False)
    secret_message_template_text = models.CharField(
        max_length=255,
        default='📩 Секретное сообщение для <b>{name}</b>',
    )
    secret_media_template_text = models.CharField(
        max_length=255,
        default="📩 Секретное медиа-сообщение для <b>{name}</b>",
    )
    secret_message_view_button_text = models.CharField(
        max_length=32,
        default="👀 Прочитать",
    )
    secret_message_delete_button_text = models.CharField(
        max_length=32,
        default="❌ Передумать",
    )
    secret_message_read_confirmation_text = models.CharField(
        max_length=255,
        default='📩 Секретное сообщение для <b>{name}</b> прочитано\n\n{text}',
    )
    secret_message_deleted_confirmation_text = models.CharField(
        max_length=255,
        default='✅ Секретное сообщение удалено',
    )
    secret_message_deleted_text = models.CharField(
        max_length=255,
        default='❌ Секретное сообщение было удалено отправителем',
    )
    secret_message_missing_text = models.CharField(
        max_length=255,
        default=(
            '😔 Сообщение не найдено.'
            ' Возможно оно ещё не загружено на наши сервера.'
            ' Попробуйте через пару секунд'
        ),
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.secret_message_template_text

    class Meta:
        constraints = (
            models.CheckConstraint(
                name='secret_message_template_text_contains_name',
                check=models.Q(secret_message_template_text__contains='{name}'),
                violation_error_message=(
                    'Secret message template text must contain "{name}"'
                ),
            ),
            models.CheckConstraint(
                name='secret_media_template_text_contains_name',
                check=models.Q(secret_media_template_text__contains='{name}'),
                violation_error_message=(
                    'Secret media template text must contain "{name}"'
                ),
            ),
            models.CheckConstraint(
                name=(
                    'secret_message_read_confirmation_text'
                    '_contains_name_and_text'
                ),
                check=(
                        models.Q(
                            secret_message_read_confirmation_text__contains='{name}')
                        & models.Q(
                    secret_message_read_confirmation_text__contains='{text}')
                ),
                violation_error_message=(
                    'Secret message read confirmation text'
                    ' must contain "{name} and {text}"'
                ),
            ),
        )


class User(models.Model):
    fullname = models.CharField(max_length=64)
    username = models.CharField(max_length=64, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    can_be_added_to_contacts = models.BooleanField(default=True)
    profile_photo_url = models.URLField(null=True, blank=True)
    is_banned = models.BooleanField(default=False)
    can_receive_notifications = models.BooleanField(default=True)
    theme = models.ForeignKey(
        to=Theme,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

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
    is_deleted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('of_user', 'to_user')

    def __str__(self):
        return self.public_name
