from django.urls import path

from holidays.views import HolidaysApi

urlpatterns = [
    path(r'', HolidaysApi.as_view(), name='holidays'),
]
