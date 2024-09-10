from typing import Final

from django.db import transaction

from economics.services import create_system_withdrawal
from users.models import Tag, User
from users.selectors.tags import TagDTO
from users.selectors.users import map_user_to_partial_dto

__all__ = (
    'delete_tag_by_id',
    'create_tag',
    'TAG_WEIGHT_TO_PRICE',
)

TAG_WEIGHT_TO_PRICE: Final[dict[Tag.Weight, int]] = {
    Tag.Weight.GOLD: 1_000_000,
    Tag.Weight.SILVER: 100_000,
    Tag.Weight.BRONZE: 10_000,
}


def delete_tag_by_id(tag_id: int) -> bool:
    deleted_count, _ = Tag.objects.filter(id=tag_id).delete()
    return bool(deleted_count)


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
    price = TAG_WEIGHT_TO_PRICE[tag.weight]
    create_system_withdrawal(
        user=of_user,
        amount=price,
        description=f'Выдача награды ({weight.label})'
    )
    return TagDTO(
        id=tag.id,
        of_user=map_user_to_partial_dto(of_user),
        to_user=map_user_to_partial_dto(to_user),
        text=tag.text,
        weight=tag.weight,
        created_at=tag.created_at,
    )
