from django.urls import path
from rest_framework.routers import DefaultRouter

from secret_messages.views import (
    ContactApi,
    SecretMessageRetrieveApi,
    SecretMessageCreateApi,
    UserContactListApi,
)

router = DefaultRouter()
router.register(r'contacts', ContactApi, basename='contact')

urlpatterns = [
    path('contacts/users/<int:user_id>/', UserContactListApi.as_view()),
    path('secret-messages/', SecretMessageCreateApi.as_view()),
    path('secret-messages/<int:pk>/', SecretMessageRetrieveApi.as_view()),
]
urlpatterns += router.urls
