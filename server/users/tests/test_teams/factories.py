import factory
from factory.django import DjangoModelFactory

from users.models import TeamMember
from users.tests.test_users.factories import UserFactory

__all__ = ('TeamFactory', 'TeamMemberFactory')


class TeamFactory(DjangoModelFactory):
    class Meta:
        model = 'users.Team'

    name = factory.Sequence(lambda n: f'team-{n}')


class TeamMemberFactory(DjangoModelFactory):
    class Meta:
        model = 'users.TeamMember'

    status = TeamMember.Status.MEMBER
    user = factory.SubFactory(UserFactory)
    team = factory.SubFactory(TeamFactory)
