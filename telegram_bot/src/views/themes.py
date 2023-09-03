from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from models import SecretMessageTheme
from views.base import View

__all__ = ('ThemeListView', 'ThemeSuccessfullyUpdatedView')


class ThemeListView(View):
    text = '✅ Тема успешно обновлена!'
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='🔙 Назад',
                    callback_data='show-personal-settings',
                ),
            ],
        ],
    )

    def __init__(self, themes: list[SecretMessageTheme]):
        self.__themes = themes

    def get_text(self) -> str:
        if not self.__themes:
            return '😔 Нет доступных тем'
        lines = [
            f'{theme.description_template_text}\n'
            f'{theme.button_text}\n'
            f'/theme_{theme.id}'
            for theme in self.__themes
        ]
        return '\n\n'.join(lines)


class ThemeSuccessfullyUpdatedView(View):
    text = '✅ Тема успешно обновлена!'
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='🔙 Назад',
                    callback_data='show-personal-settings',
                ),
            ],
        ],
    )
