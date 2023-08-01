from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class UserDoesNotExistsError(Exception):
    user_id: int
