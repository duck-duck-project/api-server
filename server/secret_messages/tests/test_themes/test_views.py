from django.urls import reverse
from rest_framework.test import APITestCase

from secret_messages.models.secret_message_themes import SecretMessageTheme


class ThemeListApiTests(APITestCase):

    def setUp(self) -> None:
        self.visible_theme = SecretMessageTheme.objects.create(
            description_template_text='📩 Секретное сообщение для <b>{name}</b>',
            button_text='👀 Прочитать',
        )
        self.hidden_theme = SecretMessageTheme.objects.create(
            description_template_text='📩 Секретная весточка для <b>{name}</b>',
            button_text='👀 Просмотреть',
            is_hidden=True,
        )

    def test_get_themes_list(self):
        url = reverse('themes')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data,
            [
                {
                    'id': self.visible_theme.id,
                    'description_template_text': (
                        self.visible_theme.description_template_text
                    ),
                    'button_text': self.visible_theme.button_text,
                },
            ],
        )
