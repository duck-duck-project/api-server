from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

__all__ = ('router',)

router = Router(name=__name__)


async def on_restart(
        message: Message,
        state: FSMContext,
) -> None:
    await state.clear()
    await message.reply('🚀 Бот перезапущен для вас')


router.message.register(
    on_restart,
    Command('restart'),
    StateFilter('*'),
)
