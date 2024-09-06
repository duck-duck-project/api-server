import random

from quizzes.exceptions import PredictionNotFoundError
from quizzes.models import Prediction

__all__ = ('get_random_prediction_text',)


def get_random_prediction_text() -> str:
    """
    Get random prediction text.

    Returns:
        Random prediction text.

    Raises:
        PredictionNotFoundError - if there are no predictions.
    """
    prediction_ids = Prediction.objects.values_list('id', flat=True)
    if not prediction_ids:
        raise PredictionNotFoundError

    try:
        return Prediction.objects.get(id=random.choice(prediction_ids)).text
    except Prediction.DoesNotExist:
        raise PredictionNotFoundError
