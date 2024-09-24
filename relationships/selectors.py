from dataclasses import dataclass
from datetime import datetime

from django.db.models import Q

from relationships.exceptions import UserHasNoRelationshipError
from relationships.models import Relationship
from users.selectors.users import UserPartialDTO, map_user_to_partial_dto

__all__ = (
    'ActiveRelationshipDTO',
    'has_active_relationship',
    'RelationshipCreateResultDTO',
    'get_active_relationship',
)


@dataclass(frozen=True, slots=True)
class RelationshipCreateResultDTO:
    id: int
    first_user: UserPartialDTO
    second_user: UserPartialDTO
    created_at: datetime


@dataclass(frozen=True, slots=True)
class ActiveRelationshipDTO:
    id: int
    first_user: UserPartialDTO
    second_user: UserPartialDTO
    created_at: datetime
    level: int
    experience: int
    experience_to_next_level: int


def has_active_relationship(user_id: int) -> bool:
    relationship = Relationship.objects.filter(
        Q(first_user_id=user_id) | Q(second_user_id=user_id),
        broke_up_at__isnull=True,
    )
    return relationship.exists()


def get_active_relationship(user_id: int) -> ActiveRelationshipDTO:
    relationship = (
        Relationship.objects
        .select_related('first_user', 'second_user')
        .filter(
            Q(first_user_id=user_id) | Q(second_user_id=user_id),
            broke_up_at__isnull=True,
        )
        .only(
            'first_user__id',
            'first_user__fullname',
            'first_user__username',
            'second_user__id',
            'second_user__fullname',
            'second_user__username',
            'created_at',
        )
        .first()
    )
    if relationship is None:
        raise UserHasNoRelationshipError

    return ActiveRelationshipDTO(
        id=relationship.id,
        first_user=map_user_to_partial_dto(relationship.first_user),
        second_user=UserPartialDTO(
            id=relationship.second_user_id,
            fullname=relationship.second_user_fullname,
            username=relationship.second_user_username,
        ),
        created_at=relationship.created_at,
    )
