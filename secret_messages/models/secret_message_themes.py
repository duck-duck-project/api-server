from django.db import models
from django.db.models import CheckConstraint

__all__ = ('SecretMessageTheme',)


class SecretMessageTheme(models.Model):
    description_template_text = models.CharField(max_length=200)
    button_text = models.CharField(max_length=32)
    description_emoji = models.CharField(max_length=16)
    button_emoji = models.CharField(max_length=16)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = (
            CheckConstraint(
                name='secret_message_template_contains_name',
                check=models.Q(text__contains='{name}'),
                violation_error_message=(
                    'Secret message template must contain "{name}"'
                ),
            ),
        )
