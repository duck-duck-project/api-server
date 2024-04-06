from django.urls import path

from wishes.views import RandomWishApi

app_name = 'wishes'
urlpatterns = [
    path(
        r'random/',
        RandomWishApi.as_view(),
        name='random-retrieve',
    ),
]
