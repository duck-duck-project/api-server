from django.urls import path

from users.views import UserRetrieveApi, UserCreateUpdateApi

urlpatterns = [
    path(r'<int:user_id>/', UserRetrieveApi.as_view()),
    path(r'', UserCreateUpdateApi.as_view()),
]
