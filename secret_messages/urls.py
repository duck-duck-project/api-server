from django.urls import path

from secret_messages.views import (
    ContactCreateUpdateApi,
    ContactRetrieveUpdateDeleteApi,
    SecretMessageRetrieveApi,
    SecretMessageCreateApi,
    UserContactListApi,
    UserSecretMediaListApi,
    SecretMediaRetrieveApi,
    SecretMediaCreateApi,
)

urlpatterns = [
    path(
        r'contacts/<int:contact_id>/',
        ContactRetrieveUpdateDeleteApi.as_view(),
    ),
    path(r'contacts/', ContactCreateUpdateApi.as_view()),
    path(r'contacts/users/<int:user_id>/', UserContactListApi.as_view()),
    path('secret-messages/', SecretMessageCreateApi.as_view()),
    path(
        'secret-messages/<uuid:secret_message_id>/',
        SecretMessageRetrieveApi.as_view(),
    ),
    path(
        r'secret-medias/users/<int:user_id>/',
        UserSecretMediaListApi.as_view(),
    ),
    path(
        r'secret-medias/<uuid:secret_media_id>/',
        SecretMediaRetrieveApi.as_view(),
    ),
    path(r'secret-medias/', SecretMediaCreateApi.as_view()),
]
