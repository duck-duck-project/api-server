from typing import TypeAlias
from uuid import uuid4

from aiogram.types import (
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ForceReply,
    ReplyKeyboardRemove,
    Message,
    InlineQueryResultArticle,
    InputTextMessageContent, CallbackQuery,
)

__all__ = (
    'ReplyMarkup',
    'View',
    'answer_view',
    'edit_message_by_view',
    'InlineQueryView',
    'render_message_or_callback_query',
    'send_view',
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
    description: str | None = None
    thumbnail_url: str | None = None
    thumbnail_width: int | None = None
    thumbnail_height: int | None = None

    def get_id(self) -> str:
        return uuid4().hex

    def get_title(self) -> str:
        return self.title

    def get_description(self) -> str | None:
        return self.description

    def get_thumbnail_url(self) -> str | None:
        return self.thumbnail_url

    def get_thumbnail_width(self) -> int | None:
        return self.thumbnail_width

    def get_thumbnail_height(self) -> int | None:
        return self.thumbnail_height

    def get_inline_query_result_article(self) -> InlineQueryResultArticle:
        return InlineQueryResultArticle(
            id=self.get_id(),
            title=self.get_title(),
            description=self.get_description(),
            input_message_content=InputTextMessageContent(
                message_text=self.get_text(),
            ),
            reply_markup=self.get_reply_markup(),
            thumb_url=self.get_thumbnail_url(),
            thumb_width=self.get_thumbnail_width(),
            thumb_height=self.get_thumbnail_height(),
        )


async def answer_view(
        *,
        message: Message,
        view: View,
        disable_web_page_preview: bool | None = None,
) -> Message:
    return await message.answer(
        text=view.get_text(),
        reply_markup=view.get_reply_markup(),
        disable_web_page_preview=disable_web_page_preview,
    )


async def edit_message_by_view(
        *,
        message: Message,
        view: View,
        disable_web_page_preview: bool | None = None,
) -> Message:
    return await message.edit_text(
        text=view.get_text(),
        reply_markup=view.get_reply_markup(),
        disable_web_page_preview=disable_web_page_preview,
    )


async def render_message_or_callback_query(
        *,
        message_or_callback_query: Message | CallbackQuery,
        view: View,
        disable_web_page_preview: bool | None = None,
) -> Message:
    match message_or_callback_query:
        case Message():
            return await answer_view(
                message=message_or_callback_query,
                view=view,
                disable_web_page_preview=disable_web_page_preview,
            )
        case CallbackQuery():
            return await edit_message_by_view(
                message=message_or_callback_query.message,
                view=view,
                disable_web_page_preview=disable_web_page_preview,
            )
        case _:
            raise ValueError('Unknown type')


async def send_view(
        *,
        bot,
        chat_id: int,
        view: View,
) -> Message:
    return await bot.send_message(
        chat_id=chat_id,
        text=view.get_text(),
        reply_markup=view.get_reply_markup(),
    )
