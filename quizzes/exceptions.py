from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException

__all__ = (
    'PredictionNotFoundError',
    'TruthOrDareQuestionNotFoundError',
    'WishNotFoundError',
)


class PredictionNotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_code = 'prediction_not_found'
    default_detail = _('Prediction was not found')


class WishNotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_code = 'wish_not_found'
    default_detail = _('Wish was not found')


class TruthOrDareQuestionNotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_code = 'truth_or_dare_question_not_found'
    default_detail = _('Truth or dare question was not found')
