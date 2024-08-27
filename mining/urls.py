from django.urls import path, register_converter

from core.converters import AnyIntConverter
from mining.views import (
    MiningActionCreateApi, MiningChatStatisticsApi, MiningUserStatisticsApi,
)

register_converter(AnyIntConverter, 'any_int')

urlpatterns = [
    path(r'', MiningActionCreateApi.as_view(), name='mining'),
    path(
        r'users/<int:user_id>/statistics/',
        MiningUserStatisticsApi.as_view(),
        name='user-statistics',
    ),
    path(
        r'chats/<any_int:user_id>/statistics/',
        MiningChatStatisticsApi.as_view(),
        name='chat-statistics',
    ),
]
