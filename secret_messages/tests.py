from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase

from secret_messages.models.secret_message_templates import (
    SecretMessageDescriptionTemplate,
)


class SecretMessageDescriptionTemplateTests(TestCase):

    def test_create_template_without_name_template(self) -> None:
        with self.assertRaisesMessage(
                IntegrityError,
                'violates check constraint'
                ' "secret_message_template_contains_name"'
        ):
            SecretMessageDescriptionTemplate.objects.create(
                text='Индивидуальная весточка',
            )


class SecretMessageDescriptionTemplateAPITests(APITestCase):

    def setUp(self) -> None:
        SecretMessageDescriptionTemplate.objects.create(
            text='💌 Индивидуальная весточка для {name}',
        )

    def test_create_secret_message_description_template(self):
        url = reverse('secret-messages-description-templates')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
