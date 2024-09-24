from django.db.models import Sum
from django.utils import timezone

from relationships.exceptions import (
    UserHasActiveRelationshipError,
)
from relationships.models import Relationship, RelationshipStarsTransaction
from relationships.selectors import (
    RelationshipCreateResultDTO,
    has_active_relationship,
)
from users.models import User
from users.selectors.users import map_user_to_partial_dto

__all__ = (
    'compute_relationship_stars_amount',
    'create_relationship',
    'validate_user_has_no_active_relationship',
    'break_up',
)


def delete_relationship(relationship_id: int | type[int]) -> None:
    Relationship.objects.filter(id=relationship_id).delete()


def validate_user_has_no_active_relationship(
        user_id: int,
) -> None:
    if has_active_relationship(user_id):
        raise UserHasActiveRelationshipError


def create_relationship(
        *,
        first_user: User,
        second_user: User,
) -> RelationshipCreateResultDTO:
    validate_user_has_no_active_relationship(first_user.id)
    validate_user_has_no_active_relationship(second_user.id)

    relationship = Relationship.objects.create(
        first_user=first_user,
        second_user=second_user,
    )
    return RelationshipCreateResultDTO(
        id=relationship.id,
        first_user=map_user_to_partial_dto(first_user),
        second_user=map_user_to_partial_dto(second_user),
        created_at=relationship.created_at,
    )


def compute_relationship_stars_amount(
        relationship_id: int | type[int],
) -> int:
    transactions = RelationshipStarsTransaction.objects.filter(
        relationship_id=relationship_id,
    )
    result = transactions.aggregate(
        stars_amount=Sum('amount', default=0)
    )
    return result['stars_amount']


def break_up(relationship_id: int) -> None:
    now = timezone.now()
    Relationship.objects.filter(id=relationship_id).update(broke_up_at=now)
