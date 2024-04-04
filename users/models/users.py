from django.db import models

from users.models.themes import Theme

__all__ = ('User',)


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
    born_on = models.DateField(null=True, blank=True)

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
        if self.born_on is None:
            return
        lifetime_delta = self.born_on.today() - self.born_on
        return int(lifetime_delta.total_seconds() / 86400)
