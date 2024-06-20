from django.db import models

from user_characteristics.models.sport_activities import SportActivity
from users.models.users import User

__all__ = ('SportActivityAction',)


class SportActivityAction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sport_activity = models.ForeignKey(SportActivity, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
