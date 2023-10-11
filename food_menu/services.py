from datetime import datetime

import httpx
from bs4 import BeautifulSoup

from food_menu.exceptions import FoodMenuApiRequestError
from food_menu.models import HTML, DailyFoodMenu, FoodMenuItem

__all__ = ('get_food_menu_html', 'parse_food_menu_html')


def get_food_menu_html() -> HTML:
    url = 'https://beslenme.manas.edu.kg/menu'
    response = httpx.get(url)
    if response.is_error:
        raise FoodMenuApiRequestError('Error while getting food menu html')
    return HTML(response.text)


def parse_daily_food_menu_html(
        *,
        food_menu_date: BeautifulSoup,
        food_menu_items: BeautifulSoup,
) -> DailyFoodMenu:
    food_menu_date = datetime.strptime(
        food_menu_date
        .text
        .strip()
        .split(' ')[0],
        '%d.%m.%Y'
    ).date()
    food_items = food_menu_items.find_all('div', attrs={'class': 'item'})

    parsed_food_items: list[FoodMenuItem] = []
    for food_item in food_items:
        photo_url: str = food_item.find('img')['src']
        food_name: str = food_item.find('h5').text.strip()

        calories_count: int = int(
            food_item.find('h6').text.strip().split(' ')[1])

        parsed_food_items.append(FoodMenuItem(
            name=food_name,
            calories_count=calories_count,
            photo_url=photo_url,
        ))

    return DailyFoodMenu(items=parsed_food_items, at=food_menu_date)


def parse_food_menu_html(html: HTML) -> list[DailyFoodMenu]:
    soup = BeautifulSoup(html, 'lxml')
    container = soup.find_all('div', attrs={'class': 'container'})[1]
    titles = container.find_all('div', attrs={'class': 'mbr-section-head'})[1:]
    bodies = container.find_all('div', attrs={'class': 'row mt-2'})

    return [
        parse_daily_food_menu_html(
            food_menu_date=date,
            food_menu_items=food_items,
        ) for date, food_items in zip(titles, bodies)
    ]
