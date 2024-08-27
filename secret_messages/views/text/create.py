from uuid import UUID

from rest_framework import serializers, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from core.exceptions import create_api_error
from secret_messages.serializers.text import SecretTextMessageSerializer
from secret_messages.services.text import create_secret_text_message
from users.exceptions import ContactDoesNotExistError
from users.selectors.contacts import get_user_contact_by_id

__all__ = ('SecretTextMessageCreateApi',)


class SecretTextMessageCreateApi(APIView):

    class InputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        text = serializers.CharField(max_length=200)
        contact_id = serializers.IntegerField()

    def post(self, request: Request) -> Response:
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        secret_text_message_id: UUID = serialized_data['id']
        text: str = serialized_data['text']
        contact_id: int = serialized_data['contact_id']

        try:
            user_contact = get_user_contact_by_id(contact_id)
        except ContactDoesNotExistError:
            raise create_api_error(
                error='contact_does_not_exist',
                status_code=status.HTTP_404_NOT_FOUND,
            )

        secret_text_message = create_secret_text_message(
            secret_text_message_id=secret_text_message_id,
            text=text,
            user_contact=user_contact
        )

        serializer = SecretTextMessageSerializer(secret_text_message)
        return Response(serializer.data, status.HTTP_201_CREATED)
