import textwrap

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from views.base import View

__all__ = (
    'PremiumSubscriptionLinkView',
    'PremiumSubscriptionInfoView',
)


class PremiumSubscriptionLinkView(View):
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='❓ Что это мне даёт',
                    callback_data='show-premium-subscription',
                ),
            ],
            [
                InlineKeyboardButton(
                    text='🚀 Купить подписку',
                    url='https://t.me/usbtypec',
                ),
            ],
        ],
    )

    def __init__(self, text):
        self.__text = text

    def get_text(self) -> str:
        return self.__text


class PremiumSubscriptionInfoView(View):
    text = textwrap.dedent('''
        ✨ <b>Преимущества премиум-подписки:</b>
        1. 📊 Увеличенный лимит на количество символов в секретных сообщениях (200 вместо 60)
        
        2. 📞 Безлимитное количество контактов (вместо ограничения в 5 для обычных пользователей)
        
        3. 💌 Анонимные сообщения в чате. Вы сможете отправлять анонимные сообщения через личку бота, которые будут пересылаться в <a href="https://studmanas.t.me">основной чат Манаса</a>.
        
        4. 🎨 Смена темы. Вы сможете менять тему секретных сообщений на любую из доступных.
        
        🔥 <b>Стоимость всего этого чуда всего 50 сомов в месяц!</b> 💰
    ''')
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='🚀 Купить подписку',
                    url='https://t.me/usbtypec',
                ),
            ],
        ],
    )
