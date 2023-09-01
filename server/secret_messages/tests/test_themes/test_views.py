from django.urls import reverse
from rest_framework.test import APITestCase

from secret_messages.tests.test_themes.factories import ThemeFactory


class ThemeListApiTests(APITestCase):

    def setUp(self) -> None:
        self.visible_theme = ThemeFactory()
        self.hidden_theme = ThemeFactory(is_hidden=True)

    def test_get_themes_list(self):
        url = reverse('themes')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data,
            {
                'themes': [
                    {
                        'id': self.visible_theme.id,
                        'description_template_text': (
                            self.visible_theme.description_template_text
                        ),
                        'button_text': self.visible_theme.button_text,
                    },
                ],
                'is_end_of_list_reached': True,
            }
        )
