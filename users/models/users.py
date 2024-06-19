from typing import Final

from django.core.validators import MaxValueValidator
from django.db import models

from users.models.nationalities import Nationality
from users.models.regions import Region
from users.models.themes import Theme

__all__ = ('User', 'USER_MAX_ENERGY', 'USER_MAX_HEALTH')

USER_MAX_ENERGY: Final[int] = 10000
USER_MAX_HEALTH: Final[int] = 10000


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

    class Gender(models.IntegerChoices):
        FEMALE = 1
        MALE = 2
        OTHER = 3

    class ContactsSortingStrategy(models.IntegerChoices):
        CREATION_TIME = 1
        PUBLIC_NAME = 2
        PRIVATE_NAME = 3

    fullname = models.CharField(max_length=64, default='Anonymous')
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
    real_first_name = models.CharField(max_length=64, null=True, blank=True)
    real_last_name = models.CharField(max_length=64, null=True, blank=True)
    patronymic = models.CharField(max_length=64, blank=True, null=True)
    gender = models.PositiveSmallIntegerField(
        choices=Gender.choices,
        null=True,
        blank=True,
    )
    nationality = models.ForeignKey(
        to=Nationality,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    region = models.ForeignKey(
        to=Region,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    contacts_sorting_strategy = models.PositiveSmallIntegerField(
        choices=ContactsSortingStrategy.choices,
        default=ContactsSortingStrategy.CREATION_TIME,
    )
    is_contacts_sorting_reversed = models.BooleanField(default=False)
    energy = models.PositiveSmallIntegerField(
        default=USER_MAX_ENERGY // 2,
        validators=(MaxValueValidator(USER_MAX_ENERGY),),
    )
    health = models.PositiveSmallIntegerField(
        default=USER_MAX_HEALTH,
        validators=(MaxValueValidator(USER_MAX_HEALTH),),
    )
    did_sports_at = models.DateTimeField(null=True, blank=True)

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
        return lifetime_delta.days
