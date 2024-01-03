from django.db import models

from users.models import User

__all__ = (
    'Department',
    'ManasId',
    'Country',
    'Nationality',
    'Region',
)


class Country(models.Model):
    name = models.CharField(max_length=64, unique=True)
    emoji = models.CharField(max_length=8)

    class Meta:
        verbose_name_plural = 'countries'

    def __str__(self):
        return f'{self.emoji} {self.name}'


class Region(models.Model):
    name = models.CharField(max_length=64, unique=True)
    country = models.ForeignKey(to=Country, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.country} | {self.name}'


class Nationality(models.Model):
    name = models.CharField(max_length=64, unique=True)

    class Meta:
        verbose_name_plural = 'nationalities'

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=64, unique=True)
    code = models.CharField(max_length=3, blank=True, null=True)
    emoji = models.CharField(max_length=8, blank=True, null=True)

    def __str__(self):
        if self.emoji is not None:
            return f'{self.emoji} {self.name}'
        return self.name


class ManasId(models.Model):

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

    class Course(models.IntegerChoices):
        PREPARATION = 1
        BACHELOR_FIRST = 2
        BACHELOR_SECOND = 3
        BACHELOR_THIRD = 4
        BACHELOR_FOURTH = 5

    class Gender(models.IntegerChoices):
        FEMALE = 1
        MALE = 2

    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    department = models.ForeignKey(to=Department, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    patronymic = models.CharField(max_length=64, blank=True, null=True)
    born_at = models.DateField()
    course = models.PositiveSmallIntegerField(choices=Course.choices)
    gender = models.PositiveSmallIntegerField(choices=Gender.choices)
    student_id = models.CharField(
        max_length=10,
        unique=True,
        null=True,
        blank=True,
        db_index=True,
    )
    obis_password = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
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
    nationality = models.ForeignKey(
        to=Nationality,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    region = models.ForeignKey(
        to=Region,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Manas ID'
        verbose_name_plural = 'Manas IDs'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def personality_type(self) -> str | None:
        is_prefix_exists = self.personality_type_prefix is not None
        is_suffix_exists = self.personality_type_suffix is not None
        if not is_prefix_exists and not is_suffix_exists:
            return None
        return f'{self.personality_type_prefix}-{self.personality_type_suffix}'

    @property
    def full_name(self) -> str:
        full_name = f'{self.first_name} {self.last_name}'
        if self.patronymic is not None:
            full_name = f'{full_name} {self.patronymic}'
        return full_name

    @property
    def document_number(self) -> str:
        abbreviated_full_name = (
            ''.join(name[0] for name in self.full_name.upper().split(' '))
        )
        born_at = f'{self.born_at:%d%m%y}'
        department_code = self.department.code or 'XXX'
        return (
            f'{self.gender}'
            f'{abbreviated_full_name}'
            f'{born_at}'
            f'{department_code}'
        )
