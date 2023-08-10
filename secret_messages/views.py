from uuid import UUID

from rest_framework import serializers, status
from rest_framework.exceptions import NotFound, APIException
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from secret_messages.exceptions import (
    ContactDoesNotExistError,
    SecretMessageDoesNotExistError,
    SecretMediaAlreadyExistsError,
)
from secret_messages.models.secret_medias import SecretMedia
from secret_messages.selectors import (
    get_contact_by_id,
    get_contacts_by_user_id,
    get_secret_message_by_id,
    get_secret_media_by_id, get_secret_medias_created_by_user_id,
)
from secret_messages.services import (
    upsert_contact, update_contact,
    create_secret_message, create_secret_media
)
from users.exceptions import UserDoesNotExistsError
from users.selectors import get_user_by_id

__all__ = (
    'UserContactListApi',
    'ContactCreateUpdateApi',
    'ContactRetrieveUpdateDeleteApi',
    'SecretMessageCreateApi',
    'SecretMessageRetrieveApi',
)


class ContactSerializer(serializers.Serializer):
    class UserSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        fullname = serializers.CharField()
        username = serializers.CharField(allow_null=True)
        is_premium = serializers.BooleanField()
        can_be_added_to_contacts = serializers.BooleanField()

    id = serializers.IntegerField()
    of_user = UserSerializer()
    to_user = UserSerializer()
    private_name = serializers.CharField()
    public_name = serializers.CharField()
    created_at = serializers.DateTimeField()
    is_hidden = serializers.BooleanField()


class UserContactListApi(APIView):

    def get(self, request: Request, user_id: int):
        contacts = get_contacts_by_user_id(user_id)
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data)


class ContactCreateUpdateApi(APIView):

    class InputSerializer(serializers.Serializer):
        of_user_id = serializers.IntegerField()
        to_user_id = serializers.IntegerField()
        private_name = serializers.CharField(max_length=64)
        public_name = serializers.CharField(max_length=64)
        is_hidden = serializers.BooleanField(default=False)

    def post(self, request: Request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        of_user_id: int = serialized_data['of_user_id']
        to_user_id: int = serialized_data['to_user_id']
        private_name: str = serialized_data['private_name']
        public_name: str = serialized_data['public_name']
        is_hidden: bool = serialized_data['is_hidden']

        try:
            of_user = get_user_by_id(of_user_id)
            to_user = get_user_by_id(to_user_id)
        except UserDoesNotExistsError as error:
            raise NotFound(f'User by ID "{error.user_id}" does not exist')

        contact, is_created = upsert_contact(
            of_user=of_user,
            to_user=to_user,
            private_name=private_name,
            public_name=public_name,
            is_hidden=is_hidden,
        )

        serializer = ContactSerializer(contact)

        status_code = (
            status.HTTP_201_CREATED
            if is_created else status.HTTP_204_NO_CONTENT
        )
        return Response(serializer.data, status=status_code)


class ContactRetrieveUpdateDeleteApi(APIView):

    class InputSerializer(serializers.Serializer):
        private_name = serializers.CharField(max_length=64)
        public_name = serializers.CharField(max_length=64)
        is_hidden = serializers.BooleanField(default=False)

    def get(self, request: Request, contact_id: int):
        try:
            contact = get_contact_by_id(contact_id)
        except ContactDoesNotExistError:
            raise NotFound('Contact does not exist')

        serializer = ContactSerializer(contact)
        return Response(serializer.data)

    def put(self, request: Request, contact_id: int):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        private_name: str = serialized_data['private_name']
        public_name: str = serialized_data['public_name']
        is_hidden: bool = serialized_data['is_hidden']

        try:
            update_contact(
                contact_id=contact_id,
                private_name=private_name,
                public_name=public_name,
                is_hidden=is_hidden,
            )
        except ContactDoesNotExistError:
            raise NotFound('Contact does not exist')

        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request: Request, contact_id: int):
        try:
            contact = get_contact_by_id(contact_id)
        except ContactDoesNotExistError:
            raise NotFound('Contact does not exist')

        contact.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


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


class UserSecretMediaListApi(APIView):

    class InputSerializer(serializers.Serializer):
        media_type = serializers.ChoiceField(
            SecretMedia.MediaType.choices,
            required=False,
        )

    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        file_id = serializers.CharField()
        name = serializers.CharField(allow_null=True)
        contact = ContactSerializer()

    def get(self, request: Request, user_id: int):
        serializer = self.InputSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        media_type: int | None = serialized_data.get('media_type')

        secret_photos = get_secret_medias_created_by_user_id(
            user_id=user_id,
            media_type=media_type,
        )
        serializer = self.OutputSerializer(secret_photos, many=True)
        return Response(serializer.data)


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
            raise NotFound('Secret photo does not exist')
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
            contact = get_contact_by_id(contact_id)
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
