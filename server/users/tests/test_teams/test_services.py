from django.test import TestCase

from users.exceptions import TeamMemberAlreadyExistsError
from users.models import User
from users.services.teams import create_team, create_team_member


class TeamCreateServicesTests(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(
            id=123456789,
            fullname='Eldos',
            username='usbtypec',
        )

    def test_create_team(self):
        team = create_team(
            user_id=self.user.id,
            name='Bulls',
        )
        self.assertEqual(team.name, 'Bulls')
        self.assertEqual(team.teammember_set.count(), 1)
        self.assertEqual(team.teammember_set.first().user, self.user)


class TeamMemberServicesTests(TestCase):

    def setUp(self) -> None:
        self.eldos = User.objects.create(
            id=123456789,
            fullname='Eldos',
            username='usbtypec',
        )
        self.alex = User.objects.create(
            id=987654321,
            fullname='Alex',
            username='alex',
        )
        self.team = create_team(
            user_id=self.eldos.id,
            name='Bulls',
        )

    def test_create_team_member(self):
        team_member = create_team_member(
            team_id=self.team.id,
            user_id=self.alex.id,
        )
        self.assertEqual(team_member.team, self.team)
        self.assertEqual(team_member.user, self.alex)
        self.assertEqual(team_member.status, team_member.Status.MEMBER)

    def test_create_team_owner_as_member(self):
        # owner is already a member
        with self.assertRaises(TeamMemberAlreadyExistsError):
            create_team_member(
                team_id=self.team.id,
                user_id=self.eldos.id,
            )
