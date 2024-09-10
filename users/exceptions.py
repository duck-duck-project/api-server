from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException

__all__ = (
    'ContactNotFoundError',
    'ContactAlreadyExistsError',
    'UserNotFoundError',
    'NotEnoughEnergyError',
    'NotEnoughHealthError',
    'SportActionCooldownError',
    'ContactAlreadyExistsError',
    'TagNotFoundError',
)


class ContactAlreadyExistsError(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = _('Contact already exists.')
    default_code = 'contact_already_exists'


class ContactNotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = _('Requested contact was not found.')
    default_code = 'contact_not_found'


class UserNotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = _('Requested user was not found.')
    default_code = 'user_not_found'


class TagNotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = _('Tag was not found')
    default_code = 'tag_not_found'


class NotEnoughEnergyError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'not_enough_energy'

    def __init__(self, required_health_value: int):
        super().__init__(
            f'User need {required_health_value} energy to perform this action.'
        )
        self.extra = {
            'required_energy_value': required_health_value,
        }


class NotEnoughHealthError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'not_enough_health'

    def __init__(self, required_health_value: int):
        super().__init__(
            f'User need {required_health_value} health to perform this action.'
        )
        self.extra = {
            'required_health_value': required_health_value,
        }


class SportActionCooldownError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'sport_action_cooldown'

    def __init__(self, next_sports_in_seconds: int):
        super().__init__(
            f'Wait {next_sports_in_seconds} seconds to perform this action.'
        )
        self.extra = {
            next_sports_in_seconds: next_sports_in_seconds,
        }
