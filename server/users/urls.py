from django.urls import path

from users.views import (
    UserRetrieveUpdateApi,
    UserCreateApi,
    UserContactListApi,
    ContactRetrieveUpdateDeleteApi,
    ContactCreateApi,
    TeamListCreateApi,
    TeamRetrieveApi,
)

app_name = 'users'
urlpatterns = [
    path(
        r'users/<int:user_id>/teams/',
        TeamListCreateApi.as_view(),
        name='teams-list-create',
    ),
    path(
        r'/teams/<int:team_id>/',
        TeamRetrieveApi.as_view(),
        name='teams-retrieve',
    ),
    path(
        r'users/<int:user_id>/',
        UserRetrieveUpdateApi.as_view(),
        name='retrieve-update',
    ),
    path(
        r'users/',
        UserCreateApi.as_view(),
        name='create',
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
]
