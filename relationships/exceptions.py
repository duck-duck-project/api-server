from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException

__all__ = (
    'UserHasNoRelationshipError',
    'UserHasActiveRelationshipError',
)


class UserHasNoRelationshipError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = _('User has no active relationship')
    default_code = 'user_has_no_relationship'


class UserHasActiveRelationshipError(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = _('User already has an active relationship')
    default_code = 'user_has_active_relationship'

    def __init__(self, user_id: int):
        super().__init__()
        self.extra = {'user_id': user_id}
