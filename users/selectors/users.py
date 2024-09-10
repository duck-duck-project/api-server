from collections.abc import Generator
from dataclasses import dataclass
from typing import Protocol

from django.db.models import QuerySet

from users.exceptions import UserNotFoundError
from users.models import User
from users.selectors.birthdays import UserPartialDTO

__all__ = (
    'get_user_by_id',
    'iter_users_with_birthdays',
    'HasIdAndFullnameAndUsername',
    'UserPartialDTO',
    'map_user_to_partial_dto',
)


class HasIdAndFullnameAndUsername(Protocol):
    id: int
    fullname: str
    username: str | None


@dataclass(frozen=True, slots=True)
class UserPartialDTO:
    id: int
    fullname: str
    username: str | None


def map_user_to_partial_dto(
        user: HasIdAndFullnameAndUsername,
) -> UserPartialDTO:
    return UserPartialDTO(
        id=user.id,
        fullname=user.fullname,
        username=user.username,
    )


def get_user_partial_by_id(user_id: int) -> UserPartialDTO:
    try:
        user = User.objects.only('id', 'fullname', 'username').get(id=user_id)
    except User.DoesNotExist:
        raise UserNotFoundError
    return map_user_to_partial_dto(user)


def get_user_by_id(user_id: int) -> User:
    """Retrieve user instance by ID. Also select related secret message theme.

    Args:
        user_id: Telegram ID of user.

    Returns:
        User instance if exists.

    Raises:
        UserDoesNotExistsError: If user does not exist.
    """
    try:
        return (
            User
            .objects
            .select_related('theme')
            .get(id=user_id)
        )
    except User.DoesNotExist:
        raise UserNotFoundError


def iter_users_with_birthdays(
        *,
        limit: int = 50,
) -> Generator[QuerySet[User], None, None]:
    offset: int = 0

    while True:
        users_with_birthdays = User.objects.exclude(born_on__isnull=True)

        ordered_by_id = users_with_birthdays.order_by('id')

        limited_users = ordered_by_id[offset:offset + limit + 1]

        yield limited_users[:limit]

        if len(limited_users) < limit:
            break

        offset += limit
