from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.filters import StateFilter, Command
from aiogram.types import Message, InputMediaPhoto

from services import get_food_menu_html, parse_food_menu_html

__all__ = ('router',)

router = Router(name=__name__)


async def on_show_food_menu(message: Message) -> None:
    food_menu_html = await get_food_menu_html()
    food_menu_items = parse_food_menu_html(food_menu_html)

    caption: list[str] = [f'🍽️ <b>Меню на сегодня</b>\n']
    for food_menu_item in food_menu_items:
        caption.append(f'▻ {food_menu_item.name}')
        caption.append(f'◦ Калории: {food_menu_item.calories}\n')

    caption_str = '\n'.join(caption)

    first = InputMediaPhoto(
        media=str(food_menu_items[0].image_url),
        caption=caption_str,
    )

    photos = [first] + [
        InputMediaPhoto(
            media=str(food_menu_item.image_url),
        ) for food_menu_item in food_menu_items[1:]
    ]

    await message.answer_media_group(media=photos)


router.message.register(
    on_show_food_menu,
    Command('yemek'),
    F.chat.type.in_({ChatType.PRIVATE, ChatType.GROUP, ChatType.SUPERGROUP}),
    StateFilter('*'),
)
