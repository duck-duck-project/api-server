from django.db import transaction, IntegrityError

from users.exceptions import TeamMemberAlreadyExistsError
from users.models import Team, TeamMember

__all__ = (
    'create_team',
    'create_team_member',
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
