from rest_framework import serializers

from users.serializers import (
    ThemeSerializer,
    UserPartialSerializer,
    UserPartialWithCanReceiveNotificationsSerializer,
)

__all__ = ('SecretTextMessageSerializer',)


class SecretTextMessageSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    text = serializers.CharField()
    sender = UserPartialSerializer()
    recipient = UserPartialWithCanReceiveNotificationsSerializer()
    theme = ThemeSerializer()
    deleted_at = serializers.DateTimeField()
    seen_at = serializers.DateTimeField()
    created_at = serializers.DateTimeField()
