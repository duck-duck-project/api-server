from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException

__all__ = (
    'SecretTextMessageIdConflictError',
    'SecretTextMessageNotFoundError',
    'SecretMediaMessageNotFoundError',
)


class SecretMediaMessageNotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = _('Secret media message not found.')
    default_code = 'secret_media_message_not_found'


class SecretTextMessageNotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = _('Secret text message not found.')
    default_code = 'secret_text_message_not_found'


class SecretTextMessageIdConflictError(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = _('Secret text message with this ID already exists.')
    default_code = 'secret_text_message_id_conflict'
