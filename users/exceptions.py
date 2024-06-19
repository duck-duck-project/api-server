from dataclasses import dataclass

__all__ = (
    'ContactDoesNotExistError',
    'ContactAlreadyExistsError',
    'UserDoesNotExistsError',
    'UserAlreadyExistsError',
    'NotEnoughEnergyError',
    'NotEnoughHealthError',
    'UserSportsThrottledError',
)


@dataclass(frozen=True, slots=True)
class UserDoesNotExistsError(Exception):
    user_id: int


class UserAlreadyExistsError(Exception):
    pass


class ContactDoesNotExistError(Exception):
    pass


class ContactAlreadyExistsError(Exception):
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
