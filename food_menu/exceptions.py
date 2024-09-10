from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException

__all__ = ('FoodMenuApiRequestError',)


class FoodMenuApiRequestError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = _('Error while requesting to food menu resource')
    default_code = 'food_menu_request_failed'
