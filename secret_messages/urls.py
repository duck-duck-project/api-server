from django.urls import path

from secret_messages.views import (
    SecretMessageRetrieveApi,
    SecretMessageCreateApi,
    SecretMediaRetrieveApi,
    SecretMediaCreateApi,
    ThemeListApi,
    ThemeRetrieveApi,
)

urlpatterns = [
    path(
        'secret-messages/',
        SecretMessageCreateApi.as_view(),
        name='secret-messages-create',
    ),
    path(
        'secret-messages/<uuid:secret_message_id>/',
        SecretMessageRetrieveApi.as_view(),
        name='secret-messages-retrieve',
    ),
    path(
        r'secret-medias/<uuid:secret_media_id>/',
        SecretMediaRetrieveApi.as_view(),
        name='secret-medias-retrieve',
    ),
    path(
        r'secret-medias/',
        SecretMediaCreateApi.as_view(),
        name='secret-medias-create',
    ),
    path(r'themes/', ThemeListApi.as_view(), name='themes-list'),
    path(
        r'themes/<int:theme_id>/',
        ThemeRetrieveApi.as_view(),
        name='themes-retrieve',
    ),
]
