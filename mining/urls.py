from django.urls import path

from mining.views import (
    MiningActionCreateApi, MiningChatStatisticsApi, MiningUserStatisticsApi,
)

urlpatterns = [
    path(r'', MiningActionCreateApi.as_view(), name='mining'),
    path(
        r'users/<int:user_id>/statistics/',
        MiningUserStatisticsApi.as_view(),
        name='user-statistics',
    ),
    path(
        r'chats/<int:user_id>/statistics/',
        MiningChatStatisticsApi.as_view(),
        name='chat-statistics',
    ),
]
