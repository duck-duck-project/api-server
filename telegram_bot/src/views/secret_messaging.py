from collections.abc import Iterable
from datetime import timedelta
from uuid import UUID

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from callback_data import (
    ContactDetailCallbackData,
    ContactUpdateCallbackData,
    ContactDeleteCallbackData,
    SecretMessageDetailCallbackData,
    InvertedSecretMessageDetailCallbackData,
)
from models import (
    Contact,
    SecretMediaType,
    SecretMedia,
    SecretMessageTheme,
)
from views import View, InlineQueryView

__all__ = (
    'ContactListView',
    'ContactDetailView',
    'SecretMessageDetailInlineQueryView',
    'EmptySecretMessageTextInlineQueryView',
    'InvertedSecretMessageDetailInlineQueryView',
    'NotPremiumUserInlineQueryView',
    'TooLongSecretMessageTextInlineQueryView',
    'NoUserContactsInlineQueryView',
    'SecretMediaCreateContactListView',
    'SecretMediaCreateConfirmView',
    'SecretMediaDetailView',
    'SecretMediaForShareView',
    'SecretMediaCalledInGroupChatView',
    'UserSettingsCalledInGroupChatView',
)


class ContactDetailView(View):

    def __init__(self, contact: Contact):
        self.__contact = contact

    def get_text(self) -> str:
        if self.__contact.to_user.username is not None:
            username = f'@{self.__contact.to_user.username}'
        else:
            username = 'нет'

        created_at_local_time = self.__contact.created_at + timedelta(hours=6)

        lines = [
            '<b>🙎🏿‍♂️ Контакт:</b>',
            f'Имя профиля: {self.__contact.to_user.fullname}',
            f'Username: {username}',
            f'Публичное имя: {self.__contact.public_name}',
            f'Приватное имя: {self.__contact.private_name}',
            f'Дата создания: {created_at_local_time:%H:%M %d.%m.%Y}'
        ]
        if self.__contact.is_hidden:
            lines.append('❗️ Скрыт в списке контактов')
        return '\n'.join(lines)

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        is_hidden_status_toggle_button_text = (
            '✅ Показать в списке контактов' if self.__contact.is_hidden
            else '❌ Скрыть из списка контактов'
        )
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text='📝 Поменять публичное имя',
                        callback_data=ContactUpdateCallbackData().new(
                            contact_id=self.__contact.id,
                            field='public_name',
                        ),
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text='📝 Поменять приватное имя',
                        callback_data=ContactUpdateCallbackData().new(
                            contact_id=self.__contact.id,
                            field='private_name',
                        ),
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text=is_hidden_status_toggle_button_text,
                        callback_data=ContactUpdateCallbackData().new(
                            contact_id=self.__contact.id,
                            field='is_hidden',
                        ),
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text='❌ Удалить',
                        callback_data=ContactDeleteCallbackData().new(
                            contact_id=self.__contact.id,
                        ),
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text='🔙 Назад',
                        callback_data='show-contacts-list',
                    ),
                ],
            ],
        )


class ContactListView(View):

    def __init__(self, contacts: Iterable[Contact]):
        self.__contacts = tuple(contacts)

    def get_text(self) -> str:
        return (
            'Список ваших контактов 👱‍♂️'
            if self.__contacts else 'У вас нет контактов 😔'
        )

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()
        for contact in self.__contacts:
            text = contact.private_name
            if contact.is_hidden:
                text = f'🙈 {text}'
            markup.row(
                InlineKeyboardButton(
                    text=text,
                    callback_data=ContactDetailCallbackData().new(
                        contact_id=contact.id,
                    ),
                ),
            )
        return markup


class InvertedSecretMessageDetailInlineQueryView(InlineQueryView):

    def __init__(
            self,
            contact: Contact,
            secret_message_id: UUID,
    ):
        self.__contact = contact
        self.__secret_message_id = secret_message_id

    def get_title(self) -> str:
        return f'Все кроме: {self.__contact.private_name}'

    def get_text(self) -> str:
        return (
            f'📩 Секретное сообщение для всех,'
            f' кроме <b>{self.__contact.public_name}</b>'
        )

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text='👀 Прочитать',
                        callback_data=(
                            InvertedSecretMessageDetailCallbackData().new(
                                contact_id=self.__contact.id,
                                secret_message_id=self.__secret_message_id.hex,
                            )
                        ),
                    )
                ]
            ]
        )


class SecretMessageDetailInlineQueryView(InlineQueryView):

    def __init__(
            self,
            query_id: UUID,
            contact: Contact,
            secret_message_id: UUID,
            secret_message_theme: SecretMessageTheme | None,
    ):
        self.__query_id = query_id
        self.__contact = contact
        self.__secret_message_id = secret_message_id
        self.__secret_message_theme = secret_message_theme

    def get_id(self) -> str:
        return self.__query_id.hex

    def get_title(self) -> str:
        return f'Контакт: {self.__contact.private_name}'

    def get_text(self) -> str:
        if self.__secret_message_theme is None:
            return (
                f'📩 Секретное сообщение для'
                f' <b>{self.__contact.public_name}</b>'
            )
        return (
            self.__secret_message_theme
            .description_template_text
            .format(name=self.__contact.public_name)
        )

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        if self.__secret_message_theme is None:
            text = '👀 Прочитать'
        else:
            text = self.__secret_message_theme.button_text
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=text,
                        callback_data=SecretMessageDetailCallbackData().new(
                            contact_id=self.__contact.id,
                            secret_message_id=self.__secret_message_id.hex,
                        ),
                    )
                ]
            ]
        )


class EmptySecretMessageTextInlineQueryView(InlineQueryView):
    title = 'Введите любой текст, который хотите отправить секретно'
    text = (
        'Я чайник 🫖\n'
        'Пойду изучать <a href="https://graph.org/Kak-otpravit'
        '-sekretnoe-soobshchenie-08-14">инструкцию</a>'
    )


class NotPremiumUserInlineQueryView(InlineQueryView):
    title = '🌟 Вы не премиум юзер'
    text = (
        'Чтобы отправить инвертированное сообщение,'
        ' вы можете приобрести премиум подписку.'
        ' Стоит она всего лишь 30 сомов в месяц.'
        ' Для покупки, напишите @usbtypec'
    )


class TooLongSecretMessageTextInlineQueryView(InlineQueryView):
    title = '❌ Слишком длинное сообщение'
    text = 'Я ввёл слишком длинное сообщение 😔'


class NoUserContactsInlineQueryView(InlineQueryView):
    title = 'У вас пока нет контактов 😔'
    text = 'У меня пока нет контактов 😔'


class SecretMediaCreateContactListView(View):

    def __init__(self, contacts: Iterable[Contact]):
        self.__contacts = tuple(contacts)

    def get_text(self) -> str:
        return (
            'Выберите контакт, которому хотите отправить медиа'
            if self.__contacts else 'У вас нет контактов 😔'
        )

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=contact.private_name,
                        callback_data=str(contact.id),
                    ),
                ] for contact in self.__contacts
            ],
        )


class SecretMediaCreateConfirmView(View):

    def __init__(
            self,
            *,
            contact: Contact,
            media_type: SecretMediaType,
            description: str | None,
    ):
        self.__contact = contact
        self.__media_type = media_type
        self.__description = description

    def get_text(self) -> str:
        if self.__description is None:
            description = ''
        else:
            description = f'с описанием "{self.__description}" '
        return (
            f'Вы уверены, что хотите отправить'
            f' секретное медиа для {description}{self.__contact.private_name}?'
        )

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text='❌ Отменить',
                        callback_data='cancel',
                    ),
                    InlineKeyboardButton(
                        text='✅ Отправить',
                        callback_data='confirm',
                    ),
                ],
            ],
        )


class SecretMediaDetailView(View):

    def __init__(self, secret_media: SecretMedia):
        self.__secret_media = secret_media

    def get_text(self) -> str:
        sender = (
                self.__secret_media.contact.of_user.username
                or self.__secret_media.contact.of_user.fullname
        )
        description = '' if self.__secret_media.name is None else (
            f'\nОписание: "{self.__secret_media.name}"'
        )
        return (
            '🖼️ Секретное медиа для'
            f' <b>{self.__secret_media.contact.public_name}</b>\n'
            f'Отправитель: {sender}'
            f'{description}'
        )


class SecretMediaForShareView(View):

    def __init__(self, *, bot_username: str, secret_media: SecretMedia):
        self.__bot_username = bot_username
        self.__secret_media = secret_media

    def get_text(self) -> str:
        return (
            '🖼️ Секретное медиа для'
            f' {self.__secret_media.contact.public_name}'
        )

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        url = (
            f'https://t.me/{self.__bot_username}'
            f'?start=secret_media-{self.__secret_media.id.hex}'
        )
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text='👀 Посмотреть',
                        url=url,
                    ),
                ]
            ]
        )


class SecretMediaCalledInGroupChatView(View):
    text = f'Отправить секретное медиа можно только через личку бота'

    def __init__(self, bot_username: str):
        self.__bot_username = bot_username

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        url = f'https://t.me/{self.__bot_username}?start=secret_media'
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=f'🚀 Отправить секретное медиа',
                        url=url,
                    ),
                ],
            ],
        )


class UserSettingsCalledInGroupChatView(View):
    text = 'Зайти в настройки можно только в личке бота'

    def __init__(self, bot_username: str):
        self.__bot_username = bot_username

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        url = f'https://t.me/{self.__bot_username}?start=settings'
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text='⚙️ Настройки профиля',
                        url=url,
                    ),
                ],
            ],
        )
