from django.urls import path

from secret_messages.views import (
    SecretMediaCreateApi, SecretMediaRetrieveApi, SecretMessageCreateApi,
    SecretMessageRetrieveUpdateDeleteApi, ContactSecretMessageListApi
)

urlpatterns = [
    path(
        'secret-messages/contacts/<int:contact_id>/',
        ContactSecretMessageListApi.as_view(),
        name='contact-secret-messages-list',
    ),
    path(
        'secret-messages/',
        SecretMessageCreateApi.as_view(),
        name='secret-messages-create',
    ),
    path(
        'secret-messages/<uuid:secret_message_id>/',
        SecretMessageRetrieveUpdateDeleteApi.as_view(),
        name='secret-messages-retrieve-update-delete',
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
]
