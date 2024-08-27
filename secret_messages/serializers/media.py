from rest_framework import serializers

from secret_messages.models.secret_medias import SecretMedia
from users.serializers import ThemeSerializer, UserPartialSerializer

__all__ = ('SecretMediaMessageSerializer',)


class SecretMediaMessageSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    file_id = serializers.CharField()
    media_type = serializers.ChoiceField(choices=SecretMedia.MediaType.choices)
    caption = serializers.CharField(allow_null=True)
    sender = UserPartialSerializer()
    recipient = UserPartialSerializer()
    theme = ThemeSerializer()
    created_at = serializers.DateTimeField()
