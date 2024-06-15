from django.urls import path

from mining.views import MiningActionCreateApi, MiningUserStatisticsApi

urlpatterns = [
    path(r'', MiningActionCreateApi.as_view(), name='mining'),
    path(
        r'user-statistics/',
        MiningUserStatisticsApi.as_view(),
        name='user-statistics',
    ),
]
