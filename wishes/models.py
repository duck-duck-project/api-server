from django.db import models

__all__ = ('Wish',)


class Wish(models.Model):
    text = models.TextField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'wishes'

    def __str__(self):
        return self.text
