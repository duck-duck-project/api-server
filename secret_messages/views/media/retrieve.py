from uuid import UUID

from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from secret_messages.models.secret_medias import SecretMedia
from secret_messages.selectors.media import get_secret_media_message
from secret_messages.serializers import SecretMediaMessageSerializer
from users.serializers import ContactSerializer

__all__ = ('SecretMediaMessageRetrieveApi',)


class SecretMediaMessageRetrieveApi(APIView):

    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        file_id = serializers.CharField()
        name = serializers.CharField(allow_null=True)
        contact = ContactSerializer()
        media_type = serializers.ChoiceField(SecretMedia.MediaType.choices)

    def get(self, request: Request, secret_media_message_id: UUID):
        secret_media_message = get_secret_media_message(secret_media_message_id)
        serializer = SecretMediaMessageSerializer(secret_media_message)
        return Response(serializer.data)
