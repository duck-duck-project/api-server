from django.test import TestCase

from secret_messages.models.secret_message_themes import SecretMessageTheme
from secret_messages.selectors import get_visible_themes


class ThemeSelectorsTests(TestCase):

    def setUp(self) -> None:
        self.hidden_theme = SecretMessageTheme.objects.create(
            description_template_text='📩 Секретное сообщение для <b>{name}</b>',
            button_text='👀 Прочитать',
            is_hidden=True,
        )
        self.visible_theme = SecretMessageTheme.objects.create(
            description_template_text=(
                '📨 Индивидуальная весточка для <b>{name}</b>'
            ),
            button_text='👓 Ознакомиться',
            is_hidden=False,
        )

    def test_get_visible_themes(self):
        visible_themes = get_visible_themes()
        self.assertEqual(len(visible_themes), 1)
        self.assertEqual(visible_themes[0].id, self.visible_theme.id)
        self.assertEqual(
            visible_themes[0].description_template_text,
            self.visible_theme.description_template_text,
        )
        self.assertEqual(
            visible_themes[0].button_text,
            self.visible_theme.button_text,
        )
        self.assertEqual(
            visible_themes[0].created_at,
            self.visible_theme.created_at,
        )
        self.assertFalse(visible_themes[0].is_hidden)
