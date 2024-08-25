from rest_framework import serializers, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from core.exceptions import create_api_error
from users.exceptions import ContactDoesNotExistError
from users.selectors.contacts import get_user_contact_by_id
from users.serializers import ContactSerializer, UserPartialWithThemeSerializer
from users.services.contacts import delete_contact_by_id, update_contact

__all__ = ('ContactRetrieveUpdateDeleteApi',)


class ContactRetrieveUpdateDeleteApi(APIView):
    class InputSerializer(serializers.Serializer):
        private_name = serializers.CharField(max_length=64)
        public_name = serializers.CharField(max_length=64)
        is_hidden = serializers.BooleanField(default=False)

    class OutputSerializer(serializers.Serializer):
        user = UserPartialWithThemeSerializer()
        contact = ContactSerializer()

    def get(self, request: Request, contact_id: int):
        try:
            user_contact = get_user_contact_by_id(contact_id)
        except ContactDoesNotExistError:
            raise create_api_error(
                error='CONTACT_DOES_NOT_EXIST',
                status_code=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.OutputSerializer(user_contact)
        response_data = {'ok': True, 'result': serializer.data}
        return Response(response_data)

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

        if not is_updated:
            raise create_api_error(
                error='CONTACT_DOES_NOT_EXIST',
                status_code=status.HTTP_404_NOT_FOUND,
            )
        return Response({'ok': True}, status=status.HTTP_200_OK)

    def delete(self, request: Request, contact_id: int):
        is_deleted = delete_contact_by_id(contact_id)
        if not is_deleted:
            raise create_api_error(
                error='CONTACT_DOES_NOT_EXIST',
                status_code=status.HTTP_404_NOT_FOUND,
            )
        return Response({'ok': True}, status=status.HTTP_200_OK)
