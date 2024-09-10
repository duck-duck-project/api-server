from typing import Final

from django.db import transaction

from economics.services import create_system_deposit, create_system_withdrawal
from users.exceptions import TagNotBelongsToUserError, TagNotFoundError
from users.models import Tag, User
from users.selectors.tags import TagDTO
from users.selectors.users import map_user_to_with_is_premium_dto

__all__ = (
    'compute_tag_issue_price',
    'compute_tag_refund_price',
    'delete_tag',
    'create_tag',
    'TAG_WEIGHT_TO_PRICE',
)

TAG_WEIGHT_TO_PRICE: Final[dict[Tag.Weight, int]] = {
    Tag.Weight.GOLD: 1_000_000,
    Tag.Weight.SILVER: 100_000,
    Tag.Weight.BRONZE: 10_000,
}


def compute_tag_issue_price(
        weight: Tag.Weight,
        is_user_premium: bool,
) -> int:
    price = TAG_WEIGHT_TO_PRICE[weight]
    return int(price * 0.75) if is_user_premium else price


def compute_tag_refund_price(
        weight: Tag.Weight,
        is_user_premium: bool,
) -> int:
    price = TAG_WEIGHT_TO_PRICE[weight]
    return int(price * 0.75) if is_user_premium else int(price * 0.5)


@transaction.atomic
def delete_tag(
        *,
        tag: TagDTO,
        user_id: int,
) -> None:
    """
    Delete existing tag if it belongs to user.

    Keyword Args:
        tag: TagDTO object.
        user_id: user's Telegram ID the tag belongs to.

    Raises:
        TagNotBelongsToUserError: if tag does not belong to user.
    """
    if tag.to_user.id != user_id:
        raise TagNotBelongsToUserError

    deleted_count, _ = Tag.objects.filter(id=tag.id).delete()

    if deleted_count == 0:
        raise TagNotFoundError

    price = compute_tag_refund_price(
        weight=tag.weight,
        is_user_premium=tag.to_user.is_premium,
    )

    create_system_deposit(
        amount=price,
        user=tag.to_user,
        description=f'Продажа награды ({tag.weight.label})',
    )


@transaction.atomic
def create_tag(
        *,
        of_user: User,
        to_user: User,
        text: str,
        weight: Tag.Weight,
) -> TagDTO:
    tag = Tag.objects.create(
        of_user=of_user,
        to_user=to_user,
        text=text,
        weight=weight,
    )
    price = compute_tag_issue_price(
        weight=weight,
        is_user_premium=of_user.is_premium,
    )
    create_system_withdrawal(
        user=of_user,
        amount=price,
        description=f'Выдача награды ({weight.label})'
    )
    return TagDTO(
        id=tag.id,
        of_user=map_user_to_with_is_premium_dto(of_user),
        to_user=map_user_to_with_is_premium_dto(to_user),
        text=tag.text,
        weight=tag.weight,
        created_at=tag.created_at,
    )
