from dataclasses import dataclass

from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException

__all__ = (
    'ContactNotFoundError',
    'ContactAlreadyExistsError',
    'UserDoesNotExistsError',
    'UserAlreadyExistsError',
    'NotEnoughEnergyError',
    'NotEnoughHealthError',
    'UserSportsThrottledError',
    'ContactDoesNotExistError',
    'ContactAlreadyExistsError',
)


class ContactAlreadyExistsError(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = _('Contact already exists.')
    default_code = 'contact_already_exists'


class ContactNotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = _('Requested contact was not found.')
    default_code = 'contact_not_found'


@dataclass(frozen=True, slots=True)
class UserDoesNotExistsError(Exception):
    user_id: int


class UserAlreadyExistsError(Exception):
    pass


class ContactDoesNotExistError(Exception):
    pass


class NotEnoughEnergyError(Exception):

    def __init__(self, cost: int):
        super().__init__('Not enough energy')
        self.cost = cost


class NotEnoughHealthError(Exception):

    def __init__(self, cost: int):
        super().__init__('Not enough health')
        self.cost = cost


class UserSportsThrottledError(Exception):

    def __init__(self, next_sports_in_seconds: int):
        super().__init__(f'Next sports in {next_sports_in_seconds} seconds')
        self.next_sports_in_seconds = next_sports_in_seconds
