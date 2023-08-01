from dataclasses import dataclass

__all__ = (
    'ContactDoesNotExistError',
    'ContactAlreadyExistsError',
)


@dataclass(frozen=True, slots=True)
class ContactDoesNotExistError(Exception):
    contact_id: int


class ContactAlreadyExistsError(Exception):
    pass
