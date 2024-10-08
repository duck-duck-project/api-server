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
    'get_relationship_by_id',
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
    next_level_experience_threshold: int


@dataclass(frozen=True, slots=True)
class RelationshipDTO:
    first_user: UserPartialDTO
    second_user: UserPartialDTO
    created_at: datetime
    level: int
    broke_up_at: datetime


def has_active_relationship(user_id: int) -> bool:
    relationship = Relationship.objects.filter(
        Q(first_user_id=user_id) | Q(second_user_id=user_id),
        broke_up_at__isnull=True,
    )
    return relationship.exists()


def get_relationship_by_id(relationship_id: int) -> RelationshipDTO:
    relationship = (
        Relationship.objects
        .select_related('first_user', 'second_user')
        .only(
            'first_user__id',
            'first_user__fullname',
            'first_user__username',
            'second_user__id',
            'second_user__fullname',
            'second_user__username',
            'experience',
            'created_at',
        )
        .get(id=relationship_id)
    )

    return RelationshipDTO(
        first_user=map_user_to_partial_dto(relationship.first_user),
        second_user=map_user_to_partial_dto(relationship.second_user),
        created_at=relationship.created_at,
        broke_up_at=relationship.broke_up_at,
        level=relationship.level,
    )


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
            'experience',
            'created_at',
        )
        .first()
    )
    if relationship is None:
        raise UserHasNoRelationshipError

    return ActiveRelationshipDTO(
        id=relationship.id,
        first_user=map_user_to_partial_dto(relationship.first_user),
        second_user=map_user_to_partial_dto(relationship.second_user),
        created_at=relationship.created_at,
        level=relationship.level,
        experience=relationship.experience,
        next_level_experience_threshold=(
            relationship.next_level_experience_threshold
        ),
    )
