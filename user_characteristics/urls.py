from django.urls import path

from user_characteristics.views.food_items import (
    FoodItemFeedApi,
    FoodItemListApi,
)
from user_characteristics.views.medicines import (
    MedicineConsumeApi,
    MedicineListApi,
)
from user_characteristics.views.sport_activities import SportActivityListApi
from user_characteristics.views.sport_activity_actions.create import \
    SportActivityActionCreateApi

urlpatterns = [
    path(r'food-items/', FoodItemListApi.as_view(), name='food-items'),
    path(
        r'food-items/feed/',
        FoodItemFeedApi.as_view(),
        name='food-items-feed',
    ),
    path(
        r'sport-activities/',
        SportActivityListApi.as_view(),
        name='sport-activities',
    ),
    path(
        r'sport-activity-actions/',
        SportActivityActionCreateApi.as_view(),
        name='sport-activity-actions',
    ),
    path(r'medicines/', MedicineListApi.as_view(), name='medicines'),
    path(
        r'medicines/consume/',
        MedicineConsumeApi.as_view(),
        name='medicines-consume',
    ),
]
