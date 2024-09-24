from django.urls import path

from relationships.views import RelationshipCreateApi, RelationshipRetrieveApi

urlpatterns = [
    path(
        r'',
        RelationshipCreateApi.as_view(),
        name='relationship-create',
    ),
    path(
        r'users/<int:user_id>/',
        RelationshipRetrieveApi.as_view(),
        name='relationship-retrieve',
    ),
]
