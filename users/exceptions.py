from dataclasses import dataclass

__all__ = (
    'ContactDoesNotExistError',
    'ContactAlreadyExistsError',
    'UserDoesNotExistsError',
    'UserAlreadyExistsError',
    'NotEnoughEnergyError',
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
