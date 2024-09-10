from django.urls import path

from user_characteristics.views.food_items import (
    FoodItemFeedApi,
    FoodItemListApi,
)
from user_characteristics.views.medicines import (
    MedicineConsumeApi,
    MedicineListApi,
)
from user_characteristics.views import SportActivityListCreateApi

urlpatterns = [
    path(r'food-items/', FoodItemListApi.as_view(), name='food-items'),
    path(
        r'food-items/feed/',
        FoodItemFeedApi.as_view(),
        name='food-items-feed',
    ),
    path(
        r'sport-activities/',
        SportActivityListCreateApi.as_view(),
        name='sport-activity-list-create',
    ),
    path(r'medicines/', MedicineListApi.as_view(), name='medicines'),
    path(
        r'medicines/consume/',
        MedicineConsumeApi.as_view(),
        name='medicines-consume',
    ),
]
