from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime

from relationships.models import Relationship
from users.models import User


@dataclass(frozen=True, slots=True)
class UserInRelationship:
    id: int
    fullname: str
    username: str | None


@dataclass(frozen=True, slots=True)
class RelationshipCreateResult:
    relationship_id: int
    user_ids: tuple[int, int]
    created_at: datetime


def delete_relationship(relationship_id: int | type[int]) -> None:
    Relationship.objects.filter(id=relationship_id).delete()


def create_relationship(
        *,
        first_user: User,
        second_user: User,
) -> RelationshipCreateResult:

    relationship = Relationship.objects.create(
        first_user=first_user,
        second_user=second_user,
    )

    return
