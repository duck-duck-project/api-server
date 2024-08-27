from django.urls import include, path

from secret_messages.views import (
    SecretMediaMessageCreateApi,
    SecretMediaMessageRetrieveApi,
    SecretTextMessageCreateApi,
    SecretTextMessageListApi,
    SecretTextMessageRetrieveDeleteApi, SecretTextMessageSeenApi,
)

secret_text_message_urlpatterns = [
    path(
        '',
        SecretTextMessageCreateApi.as_view(),
        name='secret-text-message-create',
    ),
    path(
        r'<uuid:secret_text_message_id>/',
        SecretTextMessageRetrieveDeleteApi.as_view(),
        name='secret-text-message-retrieve-delete',
    ),
    path(
        r'<uuid:secret_text_message_id>/seen/',
        SecretTextMessageSeenApi.as_view(),
        name='secret-text-message-seen',
    ),
    path(
        r'contacts/<int:contact_id>/',
        SecretTextMessageListApi.as_view(),
        name='secret-text-message-list',
    ),
]

secret_media_message_urlpatterns = [
    path(
        r'',
        SecretMediaMessageCreateApi.as_view(),
        name='secret-media-message-create',
    ),
    path(
        r'<uuid:secret_media_message_id>/',
        SecretMediaMessageRetrieveApi.as_view(),
        name='secret-media-message-retrieve',
    ),
]

urlpatterns = [
    path(r'text/', include(secret_text_message_urlpatterns)),
    path(r'media/', include(secret_media_message_urlpatterns)),
]
