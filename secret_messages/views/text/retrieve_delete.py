from uuid import UUID

from rest_framework import serializers, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from secret_messages.exceptions import SecretTextMessageNotFoundError
from secret_messages.selectors.text import get_secret_text_message_by_id
from secret_messages.serializers import SecretTextMessageSerializer
from secret_messages.services.text import delete_secret_text_message

__all__ = ('SecretTextMessageRetrieveDeleteApi',)


class SecretTextMessageRetrieveDeleteApi(APIView):

    class InputUpdateSerializer(serializers.Serializer):
        seen_at = serializers.DateTimeField()

    def get(self, request: Request, secret_text_message_id: UUID) -> Response:
        secret_text_message = get_secret_text_message_by_id(
            secret_text_message_id=secret_text_message_id,
        )
        serializer = SecretTextMessageSerializer(secret_text_message)
        return Response(serializer.data)

    def delete(
            self,
            request: Request,
            secret_text_message_id: UUID,
    ) -> Response:
        is_deleted = delete_secret_text_message(secret_text_message_id)
        if not is_deleted:
            raise SecretTextMessageNotFoundError
        return Response(status=status.HTTP_204_NO_CONTENT)
