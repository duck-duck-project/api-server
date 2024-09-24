from django.urls import path

from relationships.views import RelationCreateApi

urlpatterns = [
    path(
        r'',
        RelationCreateApi.as_view(),
        name='relationship-create',
    ),
]
