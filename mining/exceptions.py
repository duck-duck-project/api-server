from rest_framework import status
from rest_framework.exceptions import APIException

__all__ = ('MiningCooldownError',)


class MiningCooldownError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'mining_cooldown'

    def __init__(self, next_mining_in_seconds: int):
        super().__init__(
            f'Wait {next_mining_in_seconds} seconds to perform this action.'
        )
        self.extra = {
            'next_mining_in_seconds': next_mining_in_seconds,
        }
