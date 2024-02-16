from django.urls import path

from users.views import (
    ContactCreateApi, ContactRetrieveUpdateDeleteApi, TeamListCreateApi,
    TeamMemberListCreateApi, TeamMemberRetrieveDeleteApi, TeamRetrieveDeleteApi,
    UserContactListApi, UserCreateUpdateApi, UserRetrieveApi,
)

app_name = 'users'
urlpatterns = [
    path(
        'team-members/<int:team_member_id>/',
        TeamMemberRetrieveDeleteApi.as_view(),
        name='team-members-retrieve-delete',
    ),
    path(
        r'teams/<int:team_id>/members/',
        TeamMemberListCreateApi.as_view(),
        name='team-members-list-create',
    ),
    path(
        r'users/<int:user_id>/teams/',
        TeamListCreateApi.as_view(),
        name='teams-list-create',
    ),
    path(
        r'teams/<int:team_id>/',
        TeamRetrieveDeleteApi.as_view(),
        name='teams-retrieve',
    ),
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
]
