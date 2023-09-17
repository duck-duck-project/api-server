from uuid import UUID

from rest_framework import serializers, status
from rest_framework.exceptions import NotFound
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from secret_messages.exceptions import SecretMessageDoesNotExistError
from secret_messages.selectors import get_secret_message_by_id

from secret_messages.services import create_secret_message


class SecretMessageCreateApi(APIView):

    class InputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        text = serializers.CharField(max_length=200)

    def post(self, request: Request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        secret_message_id: UUID = serialized_data['id']
        text: str = serialized_data['text']

        create_secret_message(
            secret_message_id=secret_message_id,
            text=text,
        )

        return Response(status=status.HTTP_201_CREATED)


class SecretMessageRetrieveApi(APIView):

    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        text = serializers.CharField()

    def get(self, request: Request, secret_message_id: UUID):
        try:
            secret_message = get_secret_message_by_id(secret_message_id)
        except SecretMessageDoesNotExistError:
            raise NotFound('Secret message does not exist')
        serializer = self.OutputSerializer(secret_message)
        return Response(serializer.data)
