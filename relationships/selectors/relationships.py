from dataclasses import dataclass
from datetime import datetime

from django.db.models import Q

from relationships.exceptions import UserHasNoRelationshipError
from relationships.models import Relationship
from relationships.services.relationships import UserInRelationship
from users.models import User

__all__ = ('RelationshipDTO', 'get_active_relationship')


@dataclass(frozen=True, slots=True)
class RelationshipDTO:
    id: int
    first_user: UserInRelationship
    second_user: UserInRelationship
    created_at: datetime


def get_active_relationship(user: User) -> RelationshipDTO:
    user_in_relationship = UserInRelationship(
        id=user.id,
        fullname=user.fullname,
        username=user.username,
    )

    try:
        relationship = (
            Relationship.objects
            .select_related('first_user', 'second_user')
            .filter(
                Q(first_user_id=user.id) | Q(second_user_id=user.id),
                broke_up_at__isnull=True,
            )
            .values(
                'id',
                'first_user__id',
                'first_user__fullname',
                'first_user__username',
                'second_user__id',
                'second_user__fullname',
                'second_user__username',
                'created_at',
            )
        )
    except Relationship.DoesNotExist:
        raise UserHasNoRelationshipError(user_in_relationship)

    return RelationshipDTO(
        id=relationship['id'],
        first_user=UserInRelationship(
            id=relationship['first_user__id'],
            fullname=relationship['first_user__fullname'],
            username=relationship['first_user__username'],
        ),
        second_user=UserInRelationship(
            id=relationship['second_user__id'],
            fullname=relationship['second_user__fullname'],
            username=relationship['second_user__username'],
        ),
        created_at=relationship['created_at'],
    )
