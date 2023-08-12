from dataclasses import dataclass


class SecretMessageDoesNotExistError(Exception):
    pass


@dataclass(frozen=True, slots=True)
class UserDoesNotExistError(Exception):
    user_id: int


@dataclass(frozen=True, slots=True)
class UserAlreadyExistsError(Exception):
    user_id: int


class ContactAlreadyExistsError(Exception):
    pass


class SecretMediaAlreadyExistsError(Exception):
    pass


class SecretMediaDoesNotExistError(Exception):
    pass


class InvalidSecretMediaDeeplinkError(Exception):
    pass
