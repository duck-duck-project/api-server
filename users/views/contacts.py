from rest_framework import serializers, status
from rest_framework.exceptions import NotFound
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from users.exceptions import UserDoesNotExistsError, ContactDoesNotExistError
from users.selectors import (
    get_contacts_by_user_id,
    get_user_by_id,
    get_contact_by_id,
)
from users.services import upsert_contact, update_contact

__all__ = (
    'UserContactListApi',
    'ContactCreateUpdateApi',
    'ContactRetrieveUpdateDeleteApi',
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
