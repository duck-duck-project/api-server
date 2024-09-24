from django.urls import include, path

from users.views import (
    ContactCreateApi, ContactRetrieveUpdateDeleteApi, TagCreateDeleteApi,
    TagListApi, ThemeListApi, ThemeRetrieveApi, UserContactBirthdayListApi,
    UserContactListApi, UserCreateApi, user_profile_photo_upload_view,
    UserRetrieveUpdateApi,
)

users_urlpatterns = [
    path(
        r'<int:user_id>/profile-photos/',
        user_profile_photo_upload_view,
        name='user-profile-photo-upload',
    ),
    path(
        r'<int:user_id>/',
        UserRetrieveUpdateApi.as_view(),
        name='user-retrieve-update',
    ),
    path(
        r'',
        UserCreateApi.as_view(),
        name='user-create',
    ),
]

contacts_urlpatterns = [
    path(r'', ContactCreateApi.as_view(), name='contact-create'),
    path(
        r'<int:contact_id>/',
        ContactRetrieveUpdateDeleteApi.as_view(),
        name='contact-retrieve-update-delete',
    ),
    path(
        r'users/<int:user_id>/birthdays/',
        UserContactBirthdayListApi.as_view(),
        name='contact-birthdays-list',
    ),
    path(
        r'users/<int:user_id>/',
        UserContactListApi.as_view(),
        name='contact-list',
    ),
]

themes_urlpatterns = [
    path(
        r'',
        ThemeListApi.as_view(),
        name='theme-list',
    ),
    path(
        r'<uuid:theme_id>/',
        ThemeRetrieveApi.as_view(),
        name='theme-retrieve',
    ),
]

tags_urlpatterns = [
    path(
        r'',
        TagCreateDeleteApi.as_view(),
        name='tags-create-delete',
    ),
    path(
        r'users/<int:user_id>/',
        TagListApi.as_view(),
        name='tags-list',
    ),
]

app_name = 'users'
urlpatterns = [
    path(r'users/', include(users_urlpatterns)),
    path(r'contacts/', include(contacts_urlpatterns)),
    path(r'tags/', include(tags_urlpatterns)),
    path(r'themes/', include(themes_urlpatterns))
]
