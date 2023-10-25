from dataclasses import dataclass

__all__ = (
    'ContactDoesNotExistError',
    'ContactAlreadyExistsError',
    'UserDoesNotExistsError',
    'UserAlreadyExistsError',
    'TeamMemberAlreadyExistsError',
    'TeamDoesNotExistError',
    'TeamMemberDoesNotExistError',
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


class TeamMemberAlreadyExistsError(Exception):
    pass


class TeamDoesNotExistError(Exception):
    pass


class TeamMemberDoesNotExistError(Exception):
    pass
