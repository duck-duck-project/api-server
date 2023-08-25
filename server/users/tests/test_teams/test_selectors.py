from django.test import TestCase

from users.exceptions import TeamDoesNotExistError
from users.models import Team, User, TeamMember
from users.selectors.teams import (
    get_team_by_id,
    get_team_ids_and_names_by_user_id,
)


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
