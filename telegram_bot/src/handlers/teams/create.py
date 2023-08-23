from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery, Message, ChatType, ContentTypes

from repositories import HTTPClientFactory, TeamRepository
from states import TeamCreateStates
from views import TeamDetailView, answer_view

__all__ = ('register_handlers',)


async def on_start_team_creation_flow(callback_query: CallbackQuery) -> None:
    await TeamCreateStates.name.set()
    await callback_query.message.edit_text(
        '📝 Введите название секретной группы'
    )


async def on_team_name_input(
        message: Message,
        state: FSMContext,
        closing_http_client_factory: HTTPClientFactory,
) -> None:
    name = message.text
    if len(name) > 64:
        await message.reply('❌ Слишком длинное название')
        return

    async with closing_http_client_factory() as http_client:
        team_repository = TeamRepository(http_client)
        team = await team_repository.create(
            user_id=message.from_user.id,
            name=name,
        )

    await state.finish()
    await message.answer('✅ Секретная группа создана')

    view = TeamDetailView(team)
    await answer_view(message=message, view=view)


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_callback_query_handler(
        on_start_team_creation_flow,
        Text('create-team'),
        state='*',
    )
    dispatcher.register_message_handler(
        on_team_name_input,
        content_types=ContentTypes.TEXT,
        chat_type=ChatType.PRIVATE,
        state=TeamCreateStates.name,
    )
