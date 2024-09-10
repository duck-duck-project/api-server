from datetime import date, datetime, timedelta
from typing import Any
from uuid import UUID

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from users.exceptions import (
    NotEnoughEnergyError,
    NotEnoughHealthError,
    SportActionCooldownError,
)
from users.models import USER_MAX_ENERGY, USER_MAX_HEALTH, User

__all__ = (
    'upsert_user',
    'get_or_create_user',
    'increase_user_energy',
    'decrease_user_energy',
    'increase_user_health',
    'decrease_user_health',
    'do_sport_activity',
    'validate_last_sports_time',
    'consume_food',
    'update_user',
)


def upsert_user(*, user_id: int, defaults: dict[str, Any]) -> tuple[User, bool]:
    return User.objects.update_or_create(id=user_id, defaults=defaults)


def update_user(
        *,
        user_id: int,
        can_be_added_to_contacts: bool,
        theme_id: UUID | None,
        can_receive_notifications: bool,
        profile_photo_url: str | None,
        born_on: date | None,
        personality_type_prefix: str | None,
        personality_type_suffix: str | None,
        real_first_name: str | None,
        real_last_name: str | None,
        patronymic: str | None,
        gender: int,
        is_from_private_chat: bool,
):
    user = User.objects.filter(id=user_id)
    kwargs = {
        'can_be_added_to_contacts': can_be_added_to_contacts,
        'theme_id': theme_id,
        'can_receive_notifications': can_receive_notifications,
        'profile_photo_url': profile_photo_url,
        'born_on': born_on,
        'personality_type_prefix': personality_type_prefix,
        'personality_type_suffix': personality_type_suffix,
        'real_first_name': real_first_name,
        'real_last_name': real_last_name,
        'patronymic': patronymic,
        'gender': gender,
    }
    if is_from_private_chat:
        kwargs['is_blocked_bot'] = False
    updated = user.update(**kwargs)
    print(updated)


def get_or_create_user(user_id: int) -> tuple[User, bool]:
    return User.objects.get_or_create(id=user_id)


def increase_user_energy(user: User, increase: int) -> User:
    """
    Increase the energy of a user by N, ensuring it doesn't exceed the max
    limit.
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
            raise NotEnoughEnergyError(required_health_value=decrease)
        raise
    return user


def increase_user_health(user: User, increase: int) -> User:
    """
    Increase the health of a user by N, ensuring it doesn't exceed the max
    limit.
    """
    user.health = min(user.health + increase, USER_MAX_HEALTH)
    user.full_clean()
    user.save(update_fields=['health'])
    return user


def decrease_user_health(user: User, decrease: int) -> User:
    """
    Decrease the health of a user by N.
    """
    try:
        user.health -= decrease
        user.full_clean()
        user.save(update_fields=['health'])
    except ValidationError as error:
        if 'Ensure this value is greater than or equal to 0.' in error.messages:
            raise NotEnoughHealthError(required_health_value=decrease)
        raise

    return user


def compute_next_sports_time(last_sports_time: datetime) -> datetime:
    return last_sports_time + timedelta(hours=24)


def validate_last_sports_time(last_sports_time: datetime | None) -> None:
    if last_sports_time is None:
        return
    now = timezone.now()
    next_sports_time = compute_next_sports_time(last_sports_time)
    if next_sports_time > now:
        next_sports_in_seconds = int((next_sports_time - now).total_seconds())
        raise SportActionCooldownError(next_sports_in_seconds)


@transaction.atomic
def do_sport_activity(
        user: User,
        health_benefit_value: int,
        energy_cost_value: int,
) -> User:
    validate_last_sports_time(user.did_sports_at)
    user = decrease_user_energy(user, energy_cost_value)
    user.did_sports_at = timezone.now()
    user.save(update_fields=['did_sports_at'])
    return increase_user_health(user=user, increase=health_benefit_value)


@transaction.atomic
def consume_food(
        user: User,
        health_impact_value: int,
        energy: int,
) -> User:
    if health_impact_value > 0:
        user = increase_user_health(user, health_impact_value)
    elif health_impact_value < 0:
        user = decrease_user_health(user, abs(health_impact_value))
    user = increase_user_energy(user, energy)
    return user
