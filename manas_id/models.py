from django.db import models

from users.models import User

__all__ = (
    'Department',
    'ManasId',
)


class Department(models.Model):
    name = models.CharField(max_length=64, unique=True)
    code = models.CharField(max_length=3)
    emoji = models.CharField(max_length=8, blank=True, null=True)

    def __str__(self):
        if self.emoji is not None:
            return f'{self.emoji} {self.name}'
        return self.name


class ManasId(models.Model):

    class Course(models.IntegerChoices):
        PREPARATION = 1
        BACHELOR_FIRST = 2
        BACHELOR_SECOND = 3
        BACHELOR_THIRD = 4
        BACHELOR_FOURTH = 5

    class Gender(models.IntegerChoices):
        MALE = 1
        FEMALE = 2

    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    department = models.ForeignKey(to=Department, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
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
    personality_type = models.CharField(max_length=6, blank=True, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
