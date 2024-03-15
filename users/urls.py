from django.urls import path

from users.views import (
    ContactCreateApi,
    ContactRetrieveUpdateDeleteApi,
    ThemeListApi,
    ThemeRetrieveApi,
    UserContactListApi,
    UserCreateUpdateApi,
    UserRetrieveApi,
)

app_name = 'users'
urlpatterns = [
    path(
        r'users/<int:user_id>/',
        UserRetrieveApi.as_view(),
        name='retrieve',
    ),
    path(
        r'users/',
        UserCreateUpdateApi.as_view(),
        name='create-update',
    ),
    path(
        r'contacts/',
        ContactCreateApi.as_view(),
        name='contacts-create',
    ),
    path(
        r'contacts/<int:contact_id>/',
        ContactRetrieveUpdateDeleteApi.as_view(),
        name='contacts-retrieve-update-delete',
    ),
    path(
        r'users/<int:user_id>/contacts/',
        UserContactListApi.as_view(),
        name='contacts-list',
    ),
    path(
        r'themes/',
        ThemeListApi.as_view(),
        name='themes-list',
    ),
    path(
        r'themes/<uuid:theme_id>/',
        ThemeRetrieveApi.as_view(),
        name='themes-retrieve',
    ),
]
