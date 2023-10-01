from rest_framework import serializers, status
from rest_framework.exceptions import NotFound
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from users.exceptions import UserDoesNotExistsError, ContactDoesNotExistError
from users.selectors.contacts import (
    get_not_deleted_contacts_by_user_id,
    get_not_deleted_contact_by_id,
)
from users.selectors.users import get_user_by_id
from users.services.contacts import (
    update_contact, create_contact,
    delete_contact_by_id
)
from users.views.users import UserOutputSerializer

__all__ = (
    'UserContactListApi',
    'ContactCreateApi',
    'ContactRetrieveUpdateDeleteApi',
)


class ContactSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    of_user = UserOutputSerializer()
    to_user = UserOutputSerializer()
    private_name = serializers.CharField()
    public_name = serializers.CharField()
    created_at = serializers.DateTimeField()
    is_hidden = serializers.BooleanField()


class UserContactListApi(APIView):

    def get(self, request: Request, user_id: int):
        contacts = get_not_deleted_contacts_by_user_id(user_id)
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data)


class ContactCreateApi(APIView):

    class InputSerializer(serializers.Serializer):
        of_user_id = serializers.IntegerField()
        to_user_id = serializers.IntegerField()
        private_name = serializers.CharField(max_length=64)
        public_name = serializers.CharField(max_length=64)

    def post(self, request: Request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        of_user_id: int = serialized_data['of_user_id']
        to_user_id: int = serialized_data['to_user_id']
        private_name: str = serialized_data['private_name']
        public_name: str = serialized_data['public_name']

        try:
            of_user = get_user_by_id(of_user_id)
            to_user = get_user_by_id(to_user_id)
        except UserDoesNotExistsError as error:
            raise NotFound(f'User by ID "{error.user_id}" does not exist')

        contact, _ = create_contact(
            of_user=of_user,
            to_user=to_user,
            private_name=private_name,
            public_name=public_name,
        )

        serializer = ContactSerializer(contact)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ContactRetrieveUpdateDeleteApi(APIView):

    class InputSerializer(serializers.Serializer):
        private_name = serializers.CharField(max_length=64)
        public_name = serializers.CharField(max_length=64)
        is_hidden = serializers.BooleanField(default=False)

    def get(self, request: Request, contact_id: int):
        try:
            contact = get_not_deleted_contact_by_id(contact_id)
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

        is_updated = update_contact(
            contact_id=contact_id,
            private_name=private_name,
            public_name=public_name,
            is_hidden=is_hidden,
        )
        response_status_code = (
            status.HTTP_204_NO_CONTENT
            if is_updated else status.HTTP_404_NOT_FOUND
        )
        return Response(status=response_status_code)

    def delete(self, request: Request, contact_id: int):
        try:
            contact = get_not_deleted_contact_by_id(contact_id)
        except ContactDoesNotExistError:
            raise NotFound('Contact does not exist')

        is_deleted = delete_contact_by_id(contact.id)

        response_status_code = (
            status.HTTP_204_NO_CONTENT if is_deleted
            else status.HTTP_404_NOT_FOUND
        )
        return Response(status=response_status_code)