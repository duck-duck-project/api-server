from uuid import UUID

from django.utils import timezone
from rest_framework import serializers, status
from rest_framework.exceptions import NotFound
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from secret_messages.exceptions import SecretMessageDoesNotExistError
from secret_messages.selectors import get_secret_message_by_id
from secret_messages.services import create_secret_message
from users.serializers import UserSerializer


class SecretMessageSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    text = serializers.CharField()
    sender = UserSerializer()
    recipient = UserSerializer()
    is_seen = serializers.BooleanField()
    is_deleted = serializers.BooleanField()
    created_at = serializers.DateTimeField()


class SecretMessageCreateApi(APIView):
    class InputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        text = serializers.CharField(max_length=4096)
        sender_id = serializers.IntegerField()
        recipient_id = serializers.IntegerField()

    def post(self, request: Request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        secret_message_id: UUID = serialized_data['id']
        text: str = serialized_data['text']
        sender_id: int = serialized_data['sender_id']
        recipient_id: int = serialized_data['recipient_id']

        secret_message = create_secret_message(
            secret_message_id=secret_message_id,
            text=text,
            sender_id=sender_id,
            recipient_id=recipient_id,
        )

        serializer = SecretMessageSerializer(secret_message)
        response_data = {'ok': True, 'result': serializer.data}
        return Response(response_data, status=status.HTTP_201_CREATED)


class SecretMessageRetrieveUpdateDeleteApi(APIView):
    class InputUpdateSerializer(serializers.Serializer):
        is_seen = serializers.BooleanField(required=False)

    def get(self, request: Request, secret_message_id: UUID):
        try:
            secret_message = get_secret_message_by_id(secret_message_id)
        except SecretMessageDoesNotExistError:
            raise NotFound('Secret message does not exist')

        if secret_message.is_deleted:
            raise NotFound('Secret message does not exist')

        serializer = SecretMessageSerializer(secret_message)
        response_data = {'ok': True, 'result': serializer.data}
        return Response(response_data)

    def patch(self, request: Request, secret_message_id: UUID):
        serializer = self.InputUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data: dict = serializer.data

        try:
            secret_message = get_secret_message_by_id(secret_message_id)
        except SecretMessageDoesNotExistError:
            raise NotFound('Secret message does not exist')

        if secret_message.is_deleted:
            raise NotFound('Secret message does not exist')

        if 'is_seen' in serialized_data:
            secret_message.seen_at = timezone.now()

        secret_message.save()

        serializer = SecretMessageSerializer(secret_message)
        response_data = {'ok': True, 'result': serializer.data}
        return Response(response_data)

    def delete(self, request: Request, secret_message_id: UUID):
        try:
            secret_message = get_secret_message_by_id(secret_message_id)
        except SecretMessageDoesNotExistError:
            raise NotFound('Secret message does not exist')

        if secret_message.is_deleted:
            raise NotFound('Secret message does not exist')

        secret_message.deleted_at = timezone.now()
        secret_message.save()

        return Response({'ok': True})
