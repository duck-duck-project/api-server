from typing import TypeAlias
from uuid import uuid4

from aiogram.types import (
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ForceReply,
    ReplyKeyboardRemove,
    Message,
    InlineQueryResultArticle,
    InputTextMessageContent,
)

__all__ = (
    'ReplyMarkup',
    'View',
    'answer_view',
    'edit_message_by_view',
    'InlineQueryView',
)

ReplyMarkup: TypeAlias = (
        InlineKeyboardMarkup
        | ReplyKeyboardMarkup
        | ForceReply
        | ReplyKeyboardRemove
)


class View:
    text: str | None = None
    reply_markup: ReplyMarkup | None = None

    def get_text(self) -> str | None:
        return self.text

    def get_reply_markup(self) -> ReplyMarkup | None:
        return self.reply_markup


class InlineQueryView(View):
    title: str

    def get_id(self) -> str:
        return uuid4().hex

    def get_title(self) -> str:
        return self.title

    def get_inline_query_result_article(self) -> InlineQueryResultArticle:
        return InlineQueryResultArticle(
            id=self.get_id(),
            title=self.get_title(),
            input_message_content=InputTextMessageContent(self.get_text()),
            reply_markup=self.get_reply_markup(),
        )


async def answer_view(
        *,
        message: Message,
        view: View,
) -> Message:
    return await message.answer(
        text=view.get_text(),
        reply_markup=view.get_reply_markup(),
    )


async def edit_message_by_view(
        *,
        message: Message,
        view: View,
) -> Message:
    return await message.edit_text(
        text=view.get_text(),
        reply_markup=view.get_reply_markup(),
    )
