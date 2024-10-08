from uuid import UUID

from rest_framework import serializers, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from users.exceptions import ContactNotFoundError
from users.selectors.contacts import get_user_contact_by_id
from users.serializers import ContactSerializer, UserPartialWithThemeSerializer
from users.services.contacts import delete_contact_by_id, update_contact

__all__ = ('ContactRetrieveUpdateDeleteApi',)


class ContactRetrieveUpdateDeleteApi(APIView):
    class InputSerializer(serializers.Serializer):
        private_name = serializers.CharField(max_length=64)
        public_name = serializers.CharField(max_length=64)
        is_hidden = serializers.BooleanField(default=False)
        theme_id = serializers.UUIDField(allow_null=True)

    class OutputSerializer(serializers.Serializer):
        user = UserPartialWithThemeSerializer()
        contact = ContactSerializer()

    def get(self, request: Request, contact_id: int):
        user_contact = get_user_contact_by_id(contact_id)
        serializer = self.OutputSerializer(user_contact)
        return Response(serializer.data)

    def put(self, request: Request, contact_id: int):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        private_name: str = serialized_data['private_name']
        public_name: str = serialized_data['public_name']
        is_hidden: bool = serialized_data['is_hidden']
        theme_id: UUID = serialized_data['theme_id']

        is_updated = update_contact(
            contact_id=contact_id,
            private_name=private_name,
            public_name=public_name,
            is_hidden=is_hidden,
            theme_id=theme_id,
        )

        if not is_updated:
            raise ContactNotFoundError

        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request: Request, contact_id: int):
        is_deleted = delete_contact_by_id(contact_id)
        if not is_deleted:
            raise ContactNotFoundError

        return Response(status=status.HTTP_204_NO_CONTENT)
