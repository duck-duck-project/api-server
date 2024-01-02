from django.urls import path

from manas_id.views import ManasIdRetrieveApi

urlpatterns = [
    path(
        r'user-id/<int:user_id>/',
        ManasIdRetrieveApi.as_view(),
        name='manas-id-retrieve',
    ),
]
