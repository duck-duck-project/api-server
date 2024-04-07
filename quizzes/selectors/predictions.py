import random

from rest_framework.exceptions import NotFound

from quizzes.models import Prediction

__all__ = ('get_random_prediction',)


def get_random_prediction() -> Prediction:
    prediction_ids = Prediction.objects.values_list('id', flat=True)
    if not prediction_ids:
        raise NotFound('No predictions found')

    try:
        return Prediction.objects.get(id=random.choice(prediction_ids))
    except Prediction.DoesNotExist:
        raise NotFound('No predictions found')
