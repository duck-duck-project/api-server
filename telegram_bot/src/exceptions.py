from dataclasses import dataclass


class ServerAPIError(Exception):
    pass


class SecretMessageDoesNotExistError(ServerAPIError):
    pass


@dataclass(frozen=True, slots=True)
class UserDoesNotExistError(ServerAPIError):
    user_id: int

    def __str__(self):
        return f'User with Telegram ID {self.user_id} does not exist'


@dataclass(frozen=True, slots=True)
class UserAlreadyExistsError(ServerAPIError):
    user_id: int

    def __str__(self):
        return f'User with Telegram ID {self.user_id} already exists'


class ContactAlreadyExistsError(ServerAPIError):
    pass


class SecretMediaAlreadyExistsError(ServerAPIError):
    pass


class SecretMediaDoesNotExistError(ServerAPIError):
    pass


class InvalidSecretMediaDeeplinkError(Exception):
    pass


@dataclass(frozen=True, slots=True)
class ContactDoesNotExistError(ServerAPIError):
    contact_id: int

    def __str__(self) -> str:
        return f'Contact with ID {self.contact_id} does not exist'


class UserHasNoPremiumSubscriptionError(Exception):
    pass


class ThemeDoesNotExistError(ServerAPIError):
    pass
