from dataclasses import dataclass
from datetime import datetime

from users.exceptions import TagNotFoundError
from users.models.tags import Tag
from users.selectors.users import (
    UserPartialDTO, UserWithIsPremiumDTO, get_user_partial_by_id,
    map_user_to_partial_dto, map_user_to_with_is_premium_dto,
)

__all__ = (
    'TagDTO',
    'get_tag_by_id',
    'UserTagsDTO',
    'UserTagDTO',
    'get_tags_by_user_id',
)


@dataclass(frozen=True, slots=True)
class TagDTO:
    id: int
    of_user: UserWithIsPremiumDTO
    to_user: UserWithIsPremiumDTO
    text: str
    weight: Tag.Weight
    created_at: datetime


@dataclass(frozen=True, slots=True)
class UserTagDTO:
    id: int
    of_user: UserPartialDTO
    text: str
    weight: int
    created_at: datetime


@dataclass(frozen=True, slots=True)
class UserTagsDTO:
    user: UserPartialDTO
    tags: list[UserTagDTO]


def get_tag_by_number(tag_number: int) -> TagDTO:
    tag = (
        Tag.objects
        .select_related('of_user', 'to_user')
        .only(
            'id',
            'of_user__id',
            'of_user__fullname',
            'of_user__username',
            'to_user__id',
            'to_user__fullname',
            'to_user__username',
            'text',
            'weight',
            'created_at',
        )
        .order_by('weight', '-created_at')
        [tag_number - 1:tag_number]
        .first()
    )
    if tag is None:
        raise TagNotFoundError

    return TagDTO(
        id=tag.id,
        of_user=map_user_to_with_is_premium_dto(tag.of_user),
        to_user=map_user_to_with_is_premium_dto(tag.to_user),
        text=tag.text,
        weight=tag.weight,
        created_at=tag.created_at,
    )


def get_tag_by_id(tag_id: int) -> TagDTO:
    try:
        tag = (
            Tag.objects
            .select_related('of_user', 'to_user')
            .only(
                'id',
                'of_user__id',
                'of_user__fullname',
                'of_user__username',
                'to_user__id',
                'to_user__fullname',
                'to_user__username',
                'text',
                'weight',
                'created_at',
            )
            .get(id=tag_id)
        )
    except Tag.DoesNotExist:
        raise TagNotFoundError

    return TagDTO(
        id=tag.id,
        of_user=map_user_to_with_is_premium_dto(tag.of_user),
        to_user=map_user_to_with_is_premium_dto(tag.to_user),
        text=tag.text,
        weight=Tag.Weight(tag.weight),
        created_at=tag.created_at,
    )


def get_tags_by_user_id(user_id: int) -> UserTagsDTO:
    """
    Get user's tags by user's ID.

    Args:
        user_id: User's ID.

    Returns:
        UserTagsDTO object.

    Raises:
        UserNotFoundError - if user does not exist.
    """
    user_partial = get_user_partial_by_id(user_id)

    tags = (
        Tag.objects.select_related('of_user')
        .filter(to_user_id=user_id)
        .only(
            'id',
            'of_user__id',
            'of_user__fullname',
            'of_user__username',
            'to_user__id',
            'to_user__fullname',
            'to_user__username',
            'text',
            'weight',
            'created_at',
        )
        .order_by('weight', '-created_at')
        .only(
            'id',
            'of_user__id',
            'of_user__fullname',
            'of_user__username',
            'text',
            'weight',
            'created_at',
        )
    )

    user_tags = [
        UserTagDTO(
            id=tag.id,
            of_user=map_user_to_partial_dto(tag.of_user),
            text=tag.text,
            weight=tag.weight,
            created_at=tag.created_at,
        )
        for tag in tags
    ]
    return UserTagsDTO(
        user=map_user_to_partial_dto(user_partial),
        tags=user_tags,
    )
