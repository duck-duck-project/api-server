from django.urls import path

from secret_messages.views import (
    ContactCreateApi,
    ContactRetrieveUpdateDeleteApi,
    SecretMessageRetrieveApi,
    SecretMessageCreateApi,
    UserContactListApi,
)

urlpatterns = [
    path(
        r'contacts/<int:contact_id>/',
        ContactRetrieveUpdateDeleteApi.as_view(),
    ),
    path(r'contacts/', ContactCreateApi.as_view()),
    path(r'contacts/users/<int:user_id>/', UserContactListApi.as_view()),
    path('secret-messages/', SecretMessageCreateApi.as_view()),
    path('secret-messages/<int:pk>/', SecretMessageRetrieveApi.as_view()),
]
