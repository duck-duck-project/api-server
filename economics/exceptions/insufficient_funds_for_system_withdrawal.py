from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException

__all__ = ('InsufficientFundsForSystemWithdrawalError',)


class InsufficientFundsForSystemWithdrawalError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('User has insufficient funds for write-off')
    default_code = 'insufficient_funds'

    def __init__(self, amount: int):
        super().__init__()
        self.extra = {'amount': amount}
