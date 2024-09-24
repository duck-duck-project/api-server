from django.urls import path

from relationships.views import (
    RelationshipCreateApi,
    RelationshipRetrieveBreakUpApi,
)

urlpatterns = [
    path(
        r'',
        RelationshipCreateApi.as_view(),
        name='relationship-create',
    ),
    path(
        r'users/<int:user_id>/',
        RelationshipRetrieveBreakUpApi.as_view(),
        name='relationship-retrieve',
    ),
]
