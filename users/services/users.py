from typing import Any

from django.core.exceptions import ValidationError

from users.exceptions import NotEnoughEnergyError
from users.models import USER_MAX_ENERGY, User

__all__ = (
    'upsert_user',
    'get_or_create_user',
    'increase_user_energy',
    'decrease_user_energy',
)


def upsert_user(*, user_id: int, defaults: dict[str, Any]) -> tuple[User, bool]:
    return User.objects.update_or_create(id=user_id, defaults=defaults)


def get_or_create_user(user_id: int) -> tuple[User, bool]:
    return User.objects.get_or_create(id=user_id)


def increase_user_energy(user: User, increase: int) -> User:
    """
    Increase the energy of a user by N, ensuring it doesn't exceed the max limit.
    """
    user.energy = min(user.energy + increase, USER_MAX_ENERGY)
    user.full_clean()
    user.save(update_fields=['energy'])
    return user


def decrease_user_energy(user: User, decrease: int) -> User:
    """
    Decrease the energy of a user by N.
    """
    try:
        user.energy -= decrease
        user.full_clean()
        user.save(update_fields=['energy'])
    except ValidationError as error:
        if 'Ensure this value is greater than or equal to 0.' in error.messages:
            raise NotEnoughEnergyError(cost=decrease)
        raise
    return user
