from django.db import models

__all__ = ('User',)


class User(models.Model):
    fullname = models.CharField(max_length=64)
    username = models.CharField(max_length=64, null=True, blank=True)
    is_premium = models.BooleanField(default=False)
