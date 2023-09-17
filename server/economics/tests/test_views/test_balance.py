from django.urls import reverse
from rest_framework.test import APITestCase

from economics.tests.factories import SystemDepositFactory
from users.tests.test_users.factories import UserFactory


class BalanceRetrieveApiTests(APITestCase):

    def setUp(self) -> None:
        self.user = UserFactory()

    def test_user_has_no_balance(self) -> None:
        url = reverse('economics:balance-retrieve', args=(self.user.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            response.data,
            {
                'user_id': self.user.id,
                'balance': 0,
            },
        )

    def test_user_has_balance(self) -> None:
        SystemDepositFactory(
            recipient=self.user,
            amount=1000,
        )
        url = reverse('economics:balance-retrieve', args=(self.user.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            response.data,
            {
                'user_id': self.user.id,
                'balance': 1000,
            },
        )

    def test_user_not_found(self) -> None:
        url = reverse('economics:balance-retrieve', args=(12321321,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['detail'], 'User does not exists')
