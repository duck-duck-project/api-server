from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException

__all__ = (
    'InsufficientFundsForSystemWithdrawalError',
    'InsufficientFundsForTransferRollbackError',
    'InsufficientFundsForTransferError',
    'TransferSenderDoesNotMatchError',
    'TransactionIsNotTransferError',
    'TransactionDoesNotExistError',
    'TransferRollbackTimeExpiredError',
)


class InsufficientFundsForSystemWithdrawalError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('User has insufficient funds for write-off')
    default_code = 'insufficient_funds'

    def __init__(self, amount: int):
        super().__init__()
        self.extra = {'amount': amount}


class InsufficientFundsForTransferError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('User has insufficient funds for transfer')
    default_code = 'insufficient_funds'

    def __init__(self, amount: int):
        super().__init__()
        self.extra = {'amount': amount}


class InsufficientFundsForTransferRollbackError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('User has insufficient funds for transfer rollback.')
    default_code = 'insufficient_funds_for_transfer_rollback'


class TransactionDoesNotExistError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = _('User has insufficient funds for transfer rollback.')
    default_code = 'insufficient_funds_for_transfer_rollback'


class TransactionIsNotTransferError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Transaction is not a transfer.')
    default_code = 'transaction_is_not_transfer'


class TransferRollbackTimeExpiredError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Transfer rollback time has expired')
    default_code = 'transfer_rollback_time_expired'


class TransferSenderDoesNotMatchError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Transfer sender id does not match the user id')
    default_code = 'transfer_sender_does_not_match'
