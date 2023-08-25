from django.db.models import Count

from users.exceptions import TeamDoesNotExistError
from users.models import TeamMember, Team

__all__ = (
    'get_team_ids_and_names_by_user_id',
    'get_team_by_id',
    'get_team_members_by_team_id',
    'get_team_member_by_id',
)


def get_team_ids_and_names_by_user_id(user_id: int) -> list[dict]:
    """Returns team IDs and names of user.

    Args:
        user_id: ID of the user.

    Returns:
        List of dicts with team IDs and names.
    """
    return (
        Team
        .objects
        .filter(
            teammember__user_id=user_id,
            teammember__status=TeamMember.Status.OWNER,
        )
        .values('id', 'name')
    )


def get_team_by_id(team_id: int) -> Team:
    """Returns team by ID.

    Args:
        team_id: ID of the team.

    Returns:
        Team instance.
    """
    try:
        return (
            Team
            .objects
            .annotate(members_count=Count('teammember'))
            .get(id=team_id)
        )
    except Team.DoesNotExist:
        raise TeamDoesNotExistError


def get_team_members_by_team_id(team_id: int) -> list[dict]:
    """Returns team members by team ID.

    Args:
        team_id: ID of the team.

    Returns:
        List of dicts with team members.
    """
    return (
        TeamMember
        .objects
        .filter(team_id=team_id)
        .select_related('user')
        .values('id', 'user_id', 'user__fullname', 'user__username', 'status')
    )


def get_team_member_by_id(team_member_id: int) -> dict:
    """Returns team member by ID.

    Args:
        team_member_id: ID of the team member.

    Returns:
        Team member instance.

    Raises:
        TeamDoesNotExistError: If team member does not exist.
    """
    team_member = (
        TeamMember
        .objects
        .select_related('user')
        .filter(id=team_member_id)
        .values('id', 'user_id', 'user__fullname', 'user__username', 'status')
        .first()
    )
    if team_member is None:
        raise TeamDoesNotExistError
    return team_member
