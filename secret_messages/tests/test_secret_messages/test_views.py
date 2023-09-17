from uuid import uuid4

from django.urls import reverse
from rest_framework.test import APITestCase

from secret_messages.models.secret_messages import SecretMessage


class SecretMessageCreateApiTests(APITestCase):

    def test_create_secret_message(self):
        url = reverse('secret-messages-create')
        secret_message_id = uuid4()
        request_data = {
            'id': secret_message_id,
            'text': 'Hi mom!',
        }
        response = self.client.post(url, request_data)
        self.assertEqual(response.status_code, 201)

        secret_message = SecretMessage.objects.get(id=secret_message_id)
        self.assertEqual(request_data['id'], secret_message.id)
        self.assertEqual(request_data['text'], secret_message.text)


class SecretMessageRetrieveApiTests(APITestCase):

    def setUp(self) -> None:
        self.secret_message = SecretMessage.objects.create(
            id=uuid4(),
            text='Hi mom!',
        )

    def test_retrieve_secret_message(self) -> None:
        url = reverse(
            'secret-messages-retrieve',
            args=(self.secret_message.id,),
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data,
            {
                'id': str(self.secret_message.id),
                'text': self.secret_message.text,
            }
        )
