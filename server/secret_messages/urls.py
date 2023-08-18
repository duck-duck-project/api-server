from django.urls import path

from secret_messages.views import (
    SecretMessageRetrieveApi,
    SecretMessageCreateApi,
    UserSecretMediaListApi,
    SecretMediaRetrieveApi,
    SecretMediaCreateApi,
    ThemeListApi,
)

urlpatterns = [
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
    path(r'themes/', ThemeListApi.as_view(), name='themes'),
]
