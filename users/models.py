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
    class PersonalityTypeSuffix(models.TextChoices):
        ASSERTIVE = 'A', 'Assertive'
        TURBULENT = 'T', 'Turbulent'

    class PersonalityTypePrefix(models.TextChoices):
        ARCHITECT = 'INTJ', 'Стратег (INTJ)'
        LOGICIAN = 'INTP', 'Ученый (INTP)'
        COMMANDER = 'ENTJ', 'Командир (ENTJ)'
        DEBATER = 'ENTP', 'Полемист (ENTP)'
        ADVOCATE = 'INFJ', 'Активист (INFJ)'
        MEDIATOR = 'INFP', 'Посредник (INFP)'
        PROTAGONIST = 'ENFJ', 'Тренер (ENFJ)'
        CAMPAIGNER = 'ENFP', 'Борец (ENFP)'
        LOGISTICIAN = 'ISTJ', 'Администратор (ISTJ)'
        DEFENDER = 'ISFJ', 'Защитник (ISFJ)'
        EXECUTIVE = 'ESTJ', 'Менеджер (ESTJ)'
        CONSUL = 'ESFJ', 'Консул (ESFJ)'
        VIRTUOSO = 'ISTP', 'Виртуоз (ISTP)'
        ADVENTURER = 'ISFP', 'Артист (ISFP)'
        ENTREPRENEUR = 'ESTP', 'Делец (ESTP)'
        ENTERTAINER = 'ESFP', 'Развлекатель (ESFP)'

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
    is_blocked_bot = models.BooleanField(default=False)
    personality_type_prefix = models.CharField(
        max_length=4,
        choices=PersonalityTypePrefix.choices,
        null=True,
        blank=True,
    )
    personality_type_suffix = models.CharField(
        max_length=1,
        choices=PersonalityTypeSuffix.choices,
        null=True,
        blank=True,
    )
    born_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username or self.fullname

    @property
    def personality_type(self) -> str | None:
        is_prefix_exists = self.personality_type_prefix is not None
        is_suffix_exists = self.personality_type_suffix is not None
        if not is_prefix_exists and not is_suffix_exists:
            return None
        return f'{self.personality_type_prefix}-{self.personality_type_suffix}'

    @property
    def lifetime_in_days(self) -> int | None:
        if self.born_at is None:
            return
        lifetime_delta = self.born_at.today() - self.born_at
        return int(lifetime_delta.total_seconds() / 86400)


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
