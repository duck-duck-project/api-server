from collections.abc import Iterable
from uuid import UUID

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from callback_data import (
    SecretMessageDetailCallbackData,
    InvertedSecretMessageDetailCallbackData,
    SecretMessageForTeamCallbackData,
)
from models import (
    Contact,
    SecretMediaType,
    SecretMedia,
    SecretMessageTheme,
    TeamIdAndName,
)
from views import View, InlineQueryView

__all__ = (
    'SecretMessageDetailInlineQueryView',
    'SecretMessageTextMissingInlineQueryView',
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
    'SecretMessagePromptView',
    'SecretMessageNotificationView',
    'NoVisibleContactsInlineQueryView',
    'SecretMessageForTeamInlineQueryView',
)


class InvertedSecretMessageDetailInlineQueryView(InlineQueryView):

    thumbnail_width = 100
    thumbnail_height = 100

    def __init__(
            self,
            query_id: str,
            contact: Contact,
            secret_message_id: UUID,
            secret_message_theme: SecretMessageTheme | None,
    ):
        self.__query_id = query_id
        self.__contact = contact
        self.__secret_message_id = secret_message_id
        self.__secret_message_theme = secret_message_theme

    def get_id(self) -> str:
        return self.__query_id

    def get_description(self) -> str:
        return self.__contact.public_name

    def get_thumbnail_url(self) -> str | None:
        if self.__contact.to_user.profile_photo_url is None:
            return
        return str(self.__contact.to_user.profile_photo_url)

    def get_title(self) -> str:
        return f'❗️ Все кроме: {self.__contact.private_name}'

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
                            InvertedSecretMessageDetailCallbackData(
                                contact_id=self.__contact.id,
                                secret_message_id=self.__secret_message_id.hex,
                            ).pack()
                        ),
                    )
                ]
            ]
        )


class SecretMessageForTeamInlineQueryView(InlineQueryView):

    def __init__(
            self,
            query_id: str,
            team: TeamIdAndName,
            secret_message_id: UUID,
    ):
        self.__query_id = query_id
        self.__team = team
        self.__secret_message_id = secret_message_id

    def get_id(self) -> str:
        return self.__query_id

    def get_title(self) -> str:
        return f'Группа: {self.__team.name}'

    def get_description(self) -> str:
        return 'Только для участников этой секретной группы'

    def get_text(self) -> str:
        return (
            f'📩 Секретное сообщение для группы'
            f' <b>{self.__team.name}</b>'
        )

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text='👀 Прочитать',
                        callback_data=SecretMessageForTeamCallbackData(
                            team_id=self.__team.id,
                            secret_message_id=self.__secret_message_id.hex,
                        ).pack(),
                    ),
                ],
            ],
        )


class SecretMessageDetailInlineQueryView(InlineQueryView):
    thumbnail_width = 100
    thumbnail_height = 100

    def __init__(
            self,
            query_id: str,
            contact: Contact,
            secret_message_id: UUID,
            secret_message_theme: SecretMessageTheme | None,
    ):
        self.__query_id = query_id
        self.__contact = contact
        self.__secret_message_id = secret_message_id
        self.__secret_message_theme = secret_message_theme

    def get_id(self) -> str:
        return self.__query_id

    def get_description(self) -> str:
        return self.__contact.public_name

    def get_thumbnail_url(self) -> str | None:
        if self.__contact.to_user.profile_photo_url is None:
            return
        return str(self.__contact.to_user.profile_photo_url)

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
                        callback_data=SecretMessageDetailCallbackData(
                            contact_id=self.__contact.id,
                            secret_message_id=self.__secret_message_id,
                        ).pack()
                    )
                ]
            ]
        )


class SecretMessageTextMissingInlineQueryView(InlineQueryView):
    title = 'Введите любой текст, который хотите отправить секретно'
    text = (
        'Я чайник 🫖\n'
        'Пойду изучать <a href="https://graph.org/Kak-otpravit'
        '-sekretnoe-soobshchenie-08-14">инструкцию</a>'
    )
    thumbnail_url = 'https://i.imgur.com/e48C5cw.jpg'
    thumbnail_width = 100
    thumbnail_height = 100


class NotPremiumUserInlineQueryView(InlineQueryView):
    title = '🌟 Вы не премиум юзер'
    text = (
        'Чтобы отправить инвертированное сообщение,'
        ' вы можете приобрести премиум подписку.'
        ' Стоит она всего лишь 50 сомов в месяц.'
        ' Для покупки, напишите @usbtypec'
    )
    thumbnail_url = 'https://i.imgur.com/x9ruCcZ.jpg'
    thumbnail_width = 100
    thumbnail_height = 100


class TooLongSecretMessageTextInlineQueryView(InlineQueryView):
    title = '❌ Слишком длинное сообщение'
    text = 'Я ввёл слишком длинное сообщение 😔'
    thumbnail_url = 'https://i.imgur.com/gMh8VXO.jpg'
    thumbnail_height = 100
    thumbnail_width = 100


class NoUserContactsInlineQueryView(InlineQueryView):
    title = 'У вас пока нет контактов 😔'
    text = 'У меня пока нет контактов 😔'
    thumbnail_url = 'https://i.imgur.com/SfqYvom.jpeg'
    thumbnail_height = 100
    thumbnail_width = 100


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

    def __init__(
            self,
            *,
            bot_username: str,
            secret_media: SecretMedia,
            from_user_username: str,
    ):
        self.__bot_username = bot_username
        self.__secret_media = secret_media
        self.__from_user_username = from_user_username

    def get_text(self) -> str:
        return (
            '🖼️ Секретное медиа для'
            f' {self.__secret_media.contact.public_name}'
            f' от {self.__from_user_username}'
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


class SecretMessagePromptView(View):
    text = (
        '<a href="https://graph.org/Kak-otpravit-sekretnoe-soobshchenie-'
        '08-14">Инструкция</a> по отправке секретного сообщения'
    )
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='🚀 Отправить',
                    switch_inline_query_current_chat='',
                )
            ],
        ],
    )


class SecretMessageNotificationView(View):

    def __init__(
            self,
            *,
            secret_message_id: UUID,
            contact: Contact,
    ):
        self.__secret_message_id = secret_message_id
        self.__contact = contact

    def get_text(self) -> str:
        theme = self.__contact.to_user.secret_message_theme
        of_user = self.__contact.of_user
        from_username = of_user.username or of_user.fullname
        if theme is None:
            return (
                f'📩 Секретное сообщение для'
                f' <b>{self.__contact.public_name}</b>'
                f' от <b>{from_username}</b>'
            )
        text = (
            theme
            .description_template_text
            .format(name=self.__contact.public_name)
        )
        text += f'\nОт <b>{from_username}</b>'
        return text

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        theme = self.__contact.to_user.secret_message_theme
        text = '👀 Прочитать' if theme is None else theme.button_text
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=text,
                        callback_data=SecretMessageDetailCallbackData(
                            secret_message_id=self.__secret_message_id,
                            contact_id=self.__contact.id,
                        ).pack()
                    ),
                ],
            ],
        )


class NoVisibleContactsInlineQueryView(InlineQueryView):
    title = '❌ Все контакты скрыты'
    description = (
        'Перейдите в настройки бота и сделайте видимыми хотя бы один контакт'
    )
    text = 'Я скрыл все мои контакты и не могу отправить секретное сообщение 🙀'
    thumbnail_url = 'https://i.imgur.com/zAHey9P.jpg'
    thumbnail_height = 100
    thumbnail_width = 100
