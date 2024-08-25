from rest_framework import serializers, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from core.exceptions import create_api_error
from users.exceptions import ContactAlreadyExistsError
from users.serializers import ContactSerializer
from users.services.contacts import create_contact
from users.services.users import get_or_create_user

__all__ = ('ContactCreateApi',)


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

        of_user, _ = get_or_create_user(of_user_id)
        to_user, _ = get_or_create_user(to_user_id)

        try:
            contact = create_contact(
                of_user=of_user,
                to_user=to_user,
                private_name=private_name,
                public_name=public_name,
            )
        except ContactAlreadyExistsError:
            raise create_api_error(
                error='CONTACT_ALREADY_EXISTS',
                status_code=status.HTTP_409_CONFLICT,
            )

        serializer = ContactSerializer(contact)
        response_data = {'ok': True, 'result': serializer.data}
        return Response(response_data, status=status.HTTP_201_CREATED)
