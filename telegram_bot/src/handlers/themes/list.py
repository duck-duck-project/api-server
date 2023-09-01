from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery, ChatType

from repositories import HTTPClientFactory
from repositories.themes import ThemeRepository
from views import ThemeListView, edit_message_by_view

__all__ = ('register_handlers',)


async def on_show_themes_list(
        callback_query: CallbackQuery,
        state: FSMContext,
        closing_http_client_factory: HTTPClientFactory,
) -> None:
    await state.finish()

    async with closing_http_client_factory() as http_client:
        theme_repository = ThemeRepository(http_client)
        themes_page = await theme_repository.get_all(limit=100, offset=0)

    view = ThemeListView(themes_page.themes)
    await edit_message_by_view(message=callback_query.message, view=view)


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_callback_query_handler(
        on_show_themes_list,
        Text('show-themes-list'),
        chat_type=ChatType.PRIVATE,
        state='*',
    )
