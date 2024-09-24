from django.urls import path

from relationships.views import (
    RelationshipCreateApi,
    RelationshipRetrieveApi,
    RelationshipBreakUpApi,
)

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
    path(
        r'users/<int:user_id>/break-up/',
        RelationshipBreakUpApi.as_view(),
        name='relationship-break-up',
    ),
]
