from django.db import models
from django.db.models import CheckConstraint

__all__ = ('SecretMessageTheme',)


class SecretMessageTheme(models.Model):
    description_template_text = models.CharField(max_length=200)
    button_text = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    is_hidden = models.BooleanField(default=False)

    class Meta:
        constraints = (
            CheckConstraint(
                name='secret_message_template_contains_name',
                check=models.Q(description_template_text__contains='{name}'),
                violation_error_message=(
                    'Secret message template must contain "{name}"'
                ),
            ),
        )

    def __str__(self):
        return self.description_template_text
