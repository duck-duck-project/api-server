from django.urls import reverse
from rest_framework.test import APITestCase

from users.models import TeamMember
from users.tests.test_teams.factories import TeamFactory
from users.tests.test_users.factories import UserFactory


class TeamListApiTests(APITestCase):

    def setUp(self) -> None:
        self.user_1 = UserFactory()
        self.user_2 = UserFactory()
        self.team_1 = TeamFactory()
        self.team_member_1 = TeamMember.objects.create(
            team=self.team_1,
            user=self.user_1,
            status=TeamMember.Status.OWNER,
        )
        self.team_2 = TeamFactory()
        self.team_member_2 = TeamMember.objects.create(
            team=self.team_2,
            user=self.user_2,
            status=TeamMember.Status.OWNER,
        )

    def test_get(self) -> None:
        url = reverse('users:teams-list-create', args=(self.user_1.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0],
            {
                'id': self.team_1.id,
                'name': self.team_1.name,
            }
        )


class TeamCreateApiTests(APITestCase):

    def setUp(self) -> None:
        self.user = UserFactory()

    def test_post(self) -> None:
        url = reverse('users:teams-list-create', args=(self.user.id,))
        request_data = {'name': 'test_team'}
        response = self.client.post(url, request_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], request_data['name'])
        self.assertIn('id', response.data)


class TeamRetrieveApiTests(APITestCase):

    def setUp(self) -> None:
        self.team = TeamFactory()

    def test_get(self) -> None:
        url = reverse('users:teams-retrieve', args=(self.team.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], self.team.id)
        self.assertEqual(response.data['name'], self.team.name)
        self.assertEqual(response.data['members_count'], 0)
        self.assertIn('created_at', response.data)
