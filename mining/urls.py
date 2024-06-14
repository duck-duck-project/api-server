from django.urls import path

from mining.views import MiningActionCreateApi

urlpatterns = [
    path(r'', MiningActionCreateApi.as_view(), name='mining'),
]
