from django.urls import path

from users.views import (
    ContactCreateApi, ContactRetrieveUpdateDeleteApi, TagCreateApi,
    TagDeleteApi, TagListApi, ThemeListApi, ThemeRetrieveApi,
    UserContactBirthdayListApi, UserContactListApi, UserCreateUpdateApi,
    UserFoodConsumeApi, UserRetrieveApi,
)
from users.views.users import UserDoSportsApi

app_name = 'users'
urlpatterns = [
    path(
        r'users/<int:user_id>/contact-birthdays/',
        UserContactBirthdayListApi.as_view(),
        name='contact-birthdays-list',
    ),
    path(
        r'users/tags/',
        TagCreateApi.as_view(),
        name='tags-create',
    ),
    path(
        r'users/<int:user_id>/tags/<int:tag_id>/',
        TagDeleteApi.as_view(),
        name='tags-delete',
    ),
    path(
        r'users/<int:user_id>/tags/',
        TagListApi.as_view(),
        name='tags-list',
    ),
    path(
        r'users/<int:user_id>/',
        UserRetrieveApi.as_view(),
        name='retrieve',
    ),
    path(
        'users/consume-food/',
        UserFoodConsumeApi.as_view(),
        name='consume-food',
    ),
    path(
        r'users/sports/',
        UserDoSportsApi.as_view(),
        name='do-sports',
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
