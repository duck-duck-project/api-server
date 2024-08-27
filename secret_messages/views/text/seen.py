from uuid import UUID

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from secret_messages.exceptions import SecretTextMessageNotFoundError
from secret_messages.services.text import mark_secret_message_as_seen

__all__ = ('SecretTextMessageSeenApi',)


class SecretTextMessageSeenApi(APIView):

    def post(self, request: Request, secret_text_message_id: UUID) -> Response:
        is_updated = mark_secret_message_as_seen(secret_text_message_id)
        if not is_updated:
            raise SecretTextMessageNotFoundError
        return Response(status=status.HTTP_204_NO_CONTENT)
