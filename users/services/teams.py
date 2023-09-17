from django.db import transaction, IntegrityError

from users.exceptions import (
    TeamMemberAlreadyExistsError,
    TeamDoesNotExistError, TeamMemberDoesNotExistError
)
from users.models import Team, TeamMember

__all__ = (
    'create_team',
    'create_team_member',
    'delete_team_by_id',
    'delete_team_member_by_id',
)


@transaction.atomic
def create_team(
        *,
        name: str,
        user_id: int,
) -> Team:
    """Create a team and attach the user as the owner.

    Keyword Args:
        name: Name of the team.
        user_id: ID of the user to attach to the team.

    Returns:
        The created team.
    """
    team = Team.objects.create(name=name)
    TeamMember.objects.create(
        team=team,
        user_id=user_id,
        status=TeamMember.Status.OWNER,
    )
    team.members_count = 1
    return team


def create_team_member(
        *,
        team_id: int,
        user_id: int,
) -> TeamMember:
    """Create a team member attached to a specific team.

    Keyword Args:
        team_id: ID of the team to attach the member to.
        user_id: ID of the user to attach to the team.

    Returns:
        The created team member.

    Raises:
        TeamMemberAlreadyExistsError: If the user is already a member
                                      of the team.
    """
    try:
        return TeamMember.objects.create(
            team_id=team_id,
            user_id=user_id,
            status=TeamMember.Status.MEMBER,
        )
    except IntegrityError as error:
        if 'violates unique constraint' in str(error):
            raise TeamMemberAlreadyExistsError
        raise


def delete_team_by_id(team_id: int) -> None:
    """Delete a team by ID.

    Args:
        team_id: ID of the team to delete.

    Raises:
        TeamDoesNotExistError: If the team does not exist.
    """
    _, deleted_count = Team.objects.filter(id=team_id).delete()
    if not deleted_count:
        raise TeamDoesNotExistError


def delete_team_member_by_id(team_member_id: int) -> None:
    """Delete a team member by ID.

    Args:
        team_member_id: ID of the team member to delete.

    Raises:
        TeamMemberDoesNotExistError: If the team member does not exist.
    """
    _, deleted_count = TeamMember.objects.filter(id=team_member_id).delete()
    if not deleted_count:
        raise TeamMemberDoesNotExistError
