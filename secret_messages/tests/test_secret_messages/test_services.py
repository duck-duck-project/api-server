from uuid import uuid4

from django.test import TestCase

from secret_messages.models.secret_messages import SecretMessage
from secret_messages.services import create_secret_message


class SecretMessageCreateServicesTests(TestCase):

    def test_create_secret_message(self):
        secret_message_id = uuid4()
        secret_message = create_secret_message(
            secret_message_id=secret_message_id,
            text='Hello, world!',
        )
        self.assertEqual(
            secret_message,
            SecretMessage.objects.get(id=secret_message_id),
        )
