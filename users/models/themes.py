from uuid import uuid4

from django.db import models

__all__ = ('Theme',)


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
