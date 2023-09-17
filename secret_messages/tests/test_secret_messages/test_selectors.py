from uuid import uuid4

from django.test import TestCase

from secret_messages.exceptions import SecretMessageDoesNotExistError
from secret_messages.models.secret_messages import SecretMessage
from secret_messages.selectors import get_secret_message_by_id


class SecretMessageSelectorsTests(TestCase):

    def setUp(self) -> None:
        self.secret_message = SecretMessage.objects.create(
            id=uuid4(),
            text='Hi, mom',
        )

    def test_get_secret_message_by_id(self):
        secret_message = get_secret_message_by_id(self.secret_message.id)
        self.assertEqual(secret_message, self.secret_message)

    def test_get_secret_message_by_id_not_found(self):
        with self.assertRaises(SecretMessageDoesNotExistError):
            get_secret_message_by_id(uuid4())
