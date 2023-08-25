from dataclasses import dataclass

__all__ = (
    'ContactDoesNotExistError',
    'UserDoesNotExistsError',
    'UserAlreadyExistsError',
    'TeamMemberAlreadyExistsError',
)


@dataclass(frozen=True, slots=True)
class UserDoesNotExistsError(Exception):
    user_id: int


class UserAlreadyExistsError(Exception):
    pass


class ContactDoesNotExistError(Exception):
    pass


class TeamMemberAlreadyExistsError(Exception):
    pass
