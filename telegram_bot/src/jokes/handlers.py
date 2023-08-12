from aiogram import Dispatcher, Bot
from aiogram.dispatcher.filters import Command, IsReplyFilter
from aiogram.types import Message, ChatType
from aiogram.utils.exceptions import TelegramAPIError

from jokes.exceptions import JokeAlreadyExists
from jokes.repositories import JokeRepository

__all__ = ('register_handlers',)


async def on_show_statistics(
        message: Message,
        bot: Bot,
        joke_repository: JokeRepository,
) -> None:
    jokes_statistics = await joke_repository.count_by_users()

    lines: list[str] = ['<b>Статистика по шуткам за всё время (количество)</b>']

    for joke_statistics in jokes_statistics:

        try:
            chat_member = await bot.get_chat_member(
                chat_id=message.chat.id,
                user_id=joke_statistics.user_id,
            )
        except TelegramAPIError:
            continue

        name = chat_member.user.username or chat_member.user.full_name
        lines.append(f'📍 {name} - {joke_statistics.count}')

    text = '\n'.join(lines)
    await message.answer(text)


async def on_command_not_replied(
        message: Message,
) -> None:
    await message.reply(
        'Чтобы добавить шутку в реестр говно-шуток,'
        ' нужно <b>ответить на это сообщение</b>',
    )


async def on_add_joke(
        message: Message,
        reply: Message,
        joke_repository: JokeRepository,
) -> None:
    if message.from_user.id == reply.from_user.id:
        await message.reply(
            'Вы не можете добавить свою же шутку в реестр говно-шуток 😔',
        )
        return
    try:
        await joke_repository.create(
            user_id=reply.from_user.id,
            text=reply.text,
            joked_at=reply.date,
            registered_by_user_id=message.from_user.id,
        )
    except JokeAlreadyExists:
        await message.reply('Шутка уже была добавлена 😉')
    else:
        await message.reply('Добавлено в реестр говно-шуток 💩')


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_message_handler(
        on_show_statistics,
        Command('jokes_statistics'),
        state='*',
    )
    dispatcher.register_message_handler(
        on_command_not_replied,
        Command('poop'),
        IsReplyFilter(is_reply=False),
        chat_type=(ChatType.GROUP, ChatType.SUPERGROUP),
        state='*',
    )
    dispatcher.register_message_handler(
        on_add_joke,
        Command('poop'),
        IsReplyFilter(is_reply=True),
        chat_type=(ChatType.GROUP, ChatType.SUPERGROUP),
        state='*',
    )
