import contextlib

from aiogram import Router, F
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import StateFilter, Command, invert_f
from aiogram.types import Message

from filters import transfer_operation_amount_filter
from repositories import TransferRepository, UserRepository

__all__ = ('register_handlers',)


async def on_transfer_operation_amount_invalid(
        message: Message,
) -> None:
    await message.reply(
        'Чтобы осуществить перевод,'
        ' <b><u>ответьте командой</u></b> в таком формате:\n'
        '<code>/send 100</code>, где <code>100</code> - ваша сумма перевода'
    )


async def on_create_transfer_in_group_chat(
        message: Message,
        amount: int,
        transfer_repository: TransferRepository,
        user_repository: UserRepository,
) -> None:
    sender_id = message.from_user.id
    recipient_id = message.reply_to_message.from_user.id

    sender_balance = await user_repository.get_balance(sender_id)
    if sender_balance.balance < amount:
        await message.reply('❌ Недостаточно средств на балансе')
        return
    await transfer_repository.create(
        sender_id=sender_id,
        recipient_id=recipient_id,
        amount=amount,
    )
    await message.reply(f'✅ Перевод на сумму ${amount} успешно выполнен')

    recipient_balance = await user_repository.get_balance(recipient_id)
    with contextlib.suppress(TelegramAPIError):
        await message.bot.send_message(
            recipient_id,
            f'✅ Пополнение на сумму ${amount}\n'
            f'💰 Ваш баланс: ${recipient_balance.balance}',
        )


def register_handlers(router: Router) -> None:
    router.message.register(
        on_transfer_operation_amount_invalid,
        F.reply_to_message,
        Command('send'),
        invert_f(transfer_operation_amount_filter),
        StateFilter('*'),
    )
    router.message.register(
        on_create_transfer_in_group_chat,
        F.reply_to_message,
        invert_f(F.reply_to_message.from_user.is_bot),
        Command('send'),
        transfer_operation_amount_filter,
        StateFilter('*'),
    )
