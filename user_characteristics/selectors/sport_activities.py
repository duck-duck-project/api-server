from django.db.models import QuerySet

from user_characteristics.exceptions import SportActivityDoesNotExistError
from user_characteristics.models import SportActivity

__all__ = ('get_sport_activities', 'get_sport_activity_by_name')


def get_sport_activities() -> QuerySet[SportActivity]:
    return SportActivity.objects.order_by(
        'health_benefit_value',
        'energy_cost_value'
    )


def get_sport_activity_by_name(sport_activity_name: str) -> SportActivity:
    try:
        return SportActivity.objects.get(name__iexact=sport_activity_name)
    except SportActivity.DoesNotExist:
        raise SportActivityDoesNotExistError(sport_activity_name)
