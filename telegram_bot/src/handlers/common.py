from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message

__all__ = ('register_handlers',)


async def on_restart(
        message: Message,
        state: FSMContext,
) -> None:
    await state.finish()
    await message.reply('🚀 Бот перезапущен для вас')


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_message_handler(
        on_restart,
        Command('restart'),
        state='*',
    )
