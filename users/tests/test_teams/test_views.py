from django.urls import reverse
from rest_framework.test import APITestCase

from users.models import TeamMember
from users.tests.test_teams.factories import TeamFactory, TeamMemberFactory
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


class TeamMemberListApiTests(APITestCase):

    def setUp(self) -> None:
        self.team = TeamFactory()
        self.team_member_1 = TeamMemberFactory(team=self.team)
        self.team_member_2 = TeamMemberFactory()
        self.team_member_3 = TeamMemberFactory(team=self.team)
        self.team_member_4 = TeamMemberFactory()

    def test_get(self) -> None:
        url = reverse('users:team-members-list-create', args=(self.team.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(
            response.data,
            [
                {
                    'id': self.team_member_1.id,
                    'user_id': self.team_member_1.user.id,
                    'user_fullname': self.team_member_1.user.fullname,
                    'user_username': self.team_member_1.user.username,
                    'status': self.team_member_1.status.value,
                },
                {
                    'id': self.team_member_3.id,
                    'user_id': self.team_member_3.user.id,
                    'user_fullname': self.team_member_3.user.fullname,
                    'user_username': self.team_member_3.user.username,
                    'status': self.team_member_3.status.value,
                },
            ],
        )

        team_member_ids = [team_member['id'] for team_member in response.data]
        self.assertNotIn(self.team_member_2.id, team_member_ids)
        self.assertNotIn(self.team_member_4.id, team_member_ids)


class TeamMemberCreateApiTests(APITestCase):

    def setUp(self) -> None:
        self.team = TeamFactory()
        self.user = UserFactory()

    def test_post(self) -> None:
        url = reverse('users:team-members-list-create', args=(self.team.id,))
        request_data = {'user_id': self.user.id}
        response = self.client.post(url, request_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['user_id'], self.user.id)
        self.assertEqual(
            response.data['status'],
            TeamMember.Status.MEMBER.value,
        )
        self.assertIn('id', response.data)
        self.assertIn('created_at', response.data)

    def test_post_team_member_already_exists(self) -> None:
        TeamMemberFactory(team=self.team, user=self.user)
        url = reverse('users:team-members-list-create', args=(self.team.id,))
        request_data = {'user_id': self.user.id}
        response = self.client.post(url, request_data)
        self.assertEqual(response.status_code, 409)
        self.assertEqual(
            response.data,
            {'detail': 'Team member already exists'},
        )


class TeamMemberDeleteApiTests(APITestCase):

    def setUp(self) -> None:
        self.team_member = TeamMemberFactory()

    def test_delete(self) -> None:
        url = reverse(
            'users:team-members-retrieve-delete',
            args=(self.team_member.id,),
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(
            TeamMember.objects.filter(id=self.team_member.id).exists()
        )

    def test_delete_team_member_does_not_exist(self) -> None:
        url = reverse(
            'users:team-members-retrieve-delete',
            args=(self.team_member.id + 1,),
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.data,
            {'detail': 'Team member does not exist'},
        )


class TeamMemberRetrieveApiTests(APITestCase):

    def setUp(self) -> None:
        self.team_member = TeamMemberFactory()

    def test_get(self) -> None:
        url = reverse(
            'users:team-members-retrieve-delete',
            args=(self.team_member.id,),
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], self.team_member.id)
        self.assertEqual(response.data['user_id'], self.team_member.user.id)
        self.assertEqual(
            response.data['user_username'],
            self.team_member.user.username,
        )
        self.assertEqual(
            response.data['user_fullname'],
            self.team_member.user.fullname,
        )
        self.assertEqual(response.data['user_id'], self.team_member.user.id)
        self.assertEqual(response.data['status'], self.team_member.status.value)

    def test_get_team_member_does_not_exist(self) -> None:
        url = reverse(
            'users:team-members-retrieve-delete',
            args=(self.team_member.id + 1,),
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.data,
            {'detail': 'Team member does not exist'},
        )
