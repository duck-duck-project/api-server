from rest_framework import serializers, status
from rest_framework.exceptions import NotFound
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from users.exceptions import UserDoesNotExistsError
from users.selectors import get_user_by_id
from users.services import upsert_user

__all__ = (
    'UserRetrieveApi',
    'UserCreateUpdateApi',
)


class UserRetrieveApi(APIView):

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        fullname = serializers.CharField()
        username = serializers.CharField(allow_null=True)
        is_premium = serializers.BooleanField()
        can_be_added_to_contacts = serializers.BooleanField()

    def get(self, request: Request, user_id: int):
        try:
            user = get_user_by_id(user_id)
        except UserDoesNotExistsError:
            raise NotFound('User does not exist')
        serializer = self.OutputSerializer(user)
        return Response(serializer.data)


class UserCreateUpdateApi(APIView):

    class InputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        fullname = serializers.CharField(max_length=64)
        username = serializers.CharField(max_length=64, allow_null=True)
        can_be_added_to_contacts = serializers.BooleanField(default=True)

    def post(self, request: Request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        user_id: int = serialized_data['id']
        fullname: str = serialized_data['fullname']
        username: str | None = serialized_data['username']
        can_be_added_to_contacts: bool = (
            serialized_data['can_be_added_to_contacts']
        )

        _, is_created = upsert_user(
            user_id=user_id,
            fullname=fullname,
            username=username,
            can_be_added_to_contacts=can_be_added_to_contacts,
        )

        status_code = (
            status.HTTP_201_CREATED if is_created
            else status.HTTP_204_NO_CONTENT
        )
        return Response(status=status_code)
