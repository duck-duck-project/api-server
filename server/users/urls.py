from django.urls import path

from users.views import UserRetrieveUpdateApi, UserCreateApi

app_name = 'users'
urlpatterns = [
    path(
        r'<int:user_id>/',
        UserRetrieveUpdateApi.as_view(),
        name='retrieve-update',
    ),
    path(
        r'',
        UserCreateApi.as_view(),
        name='create',
    ),
]
