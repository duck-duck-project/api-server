from django.test import TestCase

from users.exceptions import TeamDoesNotExistError
from users.models import Team, User, TeamMember
from users.selectors.teams import (
    get_team_by_id,
    get_team_ids_and_names_by_user_id, get_team_members_by_team_id,
    get_team_member_by_id,
)
from users.tests.test_teams.factories import TeamMemberFactory, TeamFactory


class TeamSelectorsTests(TestCase):

    def setUp(self) -> None:
        self.eldos = User.objects.create(
            id=123456789,
            fullname='Eldos',
            username='usbtypec',
        )
        self.bulls = Team.objects.create(name='Chicago Bulls')
        TeamMember.objects.create(
            user=self.eldos,
            team=self.bulls,
            status=TeamMember.Status.OWNER,
        )

    def test_get_team_by_id(self):
        team = get_team_by_id(self.bulls.id)
        self.assertEqual(team, self.bulls)

    def test_get_team_by_id_does_not_exist_error(self):
        with self.assertRaises(TeamDoesNotExistError):
            get_team_by_id(6452578243)

    def test_get_team_ids_and_names_by_user_id(self):
        teams = get_team_ids_and_names_by_user_id(self.eldos.id)
        self.assertEqual(len(teams), 1)
        self.assertEqual(
            teams[0],
            {
                'id': self.bulls.id,
                'name': self.bulls.name,
            }
        )


class TeamMemberSelectorsTests(TestCase):

    def setUp(self) -> None:
        self.team = TeamFactory()
        self.team_member_1 = TeamMemberFactory()
        self.team_member_2 = TeamMemberFactory(team=self.team)

    def test_get_team_members_by_team_id(self) -> None:
        team_members = get_team_members_by_team_id(self.team.id)
        self.assertEqual(len(team_members), 1)
        self.assertEqual(
            team_members[0],
            {
                'id': self.team_member_2.id,
                'user_id': self.team_member_2.user_id,
                'user__fullname': self.team_member_2.user.fullname,
                'user__username': self.team_member_2.user.username,
                'status': self.team_member_2.status.value,
            }
        )

    def test_get_team_member_by_id(self) -> None:
        team_member = get_team_member_by_id(self.team_member_1.id)
        self.assertEqual(
            team_member,
            {
                'id': self.team_member_1.id,
                'user_id': self.team_member_1.user_id,
                'user__fullname': self.team_member_1.user.fullname,
                'user__username': self.team_member_1.user.username,
                'status': self.team_member_1.status.value,
            }
        )
