from typing import Any

from users.models import User

__all__ = ('upsert_user', 'get_or_create_user')


def upsert_user(*, user_id: int, defaults: dict[str, Any]) -> tuple[User, bool]:
    return User.objects.update_or_create(id=user_id, defaults=defaults)


def get_or_create_user(user_id: int) -> tuple[User, bool]:
    return User.objects.get_or_create(id=user_id)
