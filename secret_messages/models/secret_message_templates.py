from django.db import models
from django.db.models import CheckConstraint

__all__ = ('SecretMessageTemplate',)


class SecretMessageTemplate(models.Model):
    text = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = (
            CheckConstraint(
                name='secret_message_template_contains_name',
                check=models.Q(text__contains='{name}'),
            ),
        )
