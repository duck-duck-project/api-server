from uuid import UUID

from rest_framework import serializers, status
from rest_framework.exceptions import NotFound, APIException
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from secret_messages.exceptions import (
    SecretMessageDoesNotExistError,
    SecretMediaAlreadyExistsError
)
from secret_messages.models.secret_medias import SecretMedia
from secret_messages.selectors import (
    get_secret_media_by_id
)
from secret_messages.services import create_secret_media
from users.exceptions import ContactDoesNotExistError
from users.selectors.contacts import get_not_deleted_contact_by_id
from users.views.contacts import ContactSerializer


class SecretMediaRetrieveApi(APIView):

    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        file_id = serializers.CharField()
        name = serializers.CharField(allow_null=True)
        contact = ContactSerializer()
        media_type = serializers.ChoiceField(SecretMedia.MediaType.choices)

    def get(self, request: Request, secret_media_id: UUID):
        try:
            secret_photo = get_secret_media_by_id(secret_media_id)
        except SecretMessageDoesNotExistError:
            raise NotFound('Secret media does not exist')
        serializer = self.OutputSerializer(secret_photo)
        return Response(serializer.data)


class SecretMediaCreateApi(APIView):

    class InputSerializer(serializers.Serializer):
        file_id = serializers.CharField(max_length=255)
        name = serializers.CharField(max_length=64, allow_null=True)
        contact_id = serializers.IntegerField()
        media_type = serializers.ChoiceField(
            choices=SecretMedia.MediaType.choices,
        )

    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        file_id = serializers.CharField()
        name = serializers.CharField(allow_null=True)
        contact = ContactSerializer()
        media_type = serializers.IntegerField()

    def post(self, request: Request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        file_id: str = serialized_data['file_id']
        name: str | None = serialized_data['name']
        contact_id: int = serialized_data['contact_id']
        media_type: int = serialized_data['media_type']

        try:
            contact = get_not_deleted_contact_by_id(contact_id)
        except ContactDoesNotExistError:
            raise NotFound('Contact does not exist')

        try:
            secret_photo = create_secret_media(
                file_id=file_id,
                name=name,
                contact=contact,
                media_type=media_type,
            )
        except SecretMediaAlreadyExistsError:
            error = APIException(
                f'Secret media with file ID "{file_id}" already exists',
            )
            error.status_code = status.HTTP_409_CONFLICT
            raise error

        serializer = self.OutputSerializer(secret_photo)
        response_data = serializer.data

        return Response(response_data, status=status.HTTP_201_CREATED)
