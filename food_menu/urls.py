from django.urls import path

from food_menu.views import FoodMenuApi

urlpatterns = [
    path(r'food-menu/', FoodMenuApi.as_view(), name='food-menu'),
]
