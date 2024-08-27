from rest_framework import serializers, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from secret_messages.models import SecretMedia
from secret_messages.serializers import SecretMediaMessageSerializer
from secret_messages.services.media import create_secret_media_message
from users.selectors.contacts import get_user_contact_by_id

__all__ = ('SecretMediaMessageCreateApi',)


class SecretMediaMessageCreateApi(APIView):

    class InputSerializer(serializers.Serializer):
        file_id = serializers.CharField(max_length=255)
        caption = serializers.CharField(max_length=64, allow_null=True)
        contact_id = serializers.IntegerField()
        media_type = serializers.ChoiceField(
            choices=SecretMedia.MediaType.choices,
        )

    def post(self, request: Request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        file_id: str = serialized_data['file_id']
        caption: str | None = serialized_data['caption']
        contact_id: int = serialized_data['contact_id']
        media_type: int = serialized_data['media_type']

        user_contact = get_user_contact_by_id(contact_id)
        secret_media_message = create_secret_media_message(
            file_id=file_id,
            caption=caption,
            user_contact=user_contact,
            media_type=media_type,
        )

        serializer = SecretMediaMessageSerializer(secret_media_message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
