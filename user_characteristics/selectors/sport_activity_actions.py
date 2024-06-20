from user_characteristics.models import SportActivityAction
from users.models import User

__all__ = ('get_last_sport_activity_action',)


def get_last_sport_activity_action(user: User) -> SportActivityAction | None:
    return (
        SportActivityAction.objects
        .select_related('sport_activity')
        .filter(user=user)
        .order_by('-created_at')
        .first()
    )
