from django.db import models

__all__ = (
    'TruthOrDareQuestion',
    'Wish',
    'Prediction',
)


class TruthOrDareQuestion(models.Model):
    class Type(models.IntegerChoices):
        TRUTH = 1
        DARE = 2

    text = models.CharField(max_length=200, unique=True)
    type = models.PositiveSmallIntegerField(choices=Type.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


class Wish(models.Model):
    text = models.TextField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'wishes'

    def __str__(self):
        return self.text


class Prediction(models.Model):
    text = models.TextField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
