from django.urls import path

urlpatterns = [
    path(r'users/<int:user_id>/'),
]