from django.test import TestCase

from secret_messages.exceptions import ThemeDoesNotExistError
from secret_messages.selectors import get_visible_themes, get_theme_by_id
from secret_messages.tests.test_themes.factories import ThemeFactory


class ThemeSelectorsTests(TestCase):

    def setUp(self) -> None:
        self.hidden_theme = ThemeFactory(is_hidden=True)
        self.visible_theme = ThemeFactory()

    def test_get_visible_themes(self):
        visible_themes = get_visible_themes(limit=100, offset=0)
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

    def test_offset(self):
        visible_themes = get_visible_themes(limit=100, offset=1)
        self.assertEqual(len(visible_themes), 0)

    def test_get_theme_by_id(self) -> None:
        theme = get_theme_by_id(self.visible_theme.id)
        self.assertEqual(theme.id, self.visible_theme.id)

    def test_get_theme_by_id_theme_does_not_exist(self) -> None:
        with self.assertRaises(ThemeDoesNotExistError):
            get_theme_by_id(self.visible_theme.id + 1)
