from datetime import date

from rest_framework import serializers, status
from rest_framework.exceptions import NotFound, APIException
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from users.exceptions import UserDoesNotExistsError, UserAlreadyExistsError
from users.selectors.users import get_user_by_id
from users.services.users import update_user, create_user

__all__ = (
    'UserRetrieveUpdateApi',
    'UserCreateApi',
)


class UserOutputSerializer(serializers.Serializer):

    class SecretMessageThemeSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        description_template_text = serializers.CharField()
        button_text = serializers.CharField()
        is_hidden = serializers.BooleanField()

    id = serializers.IntegerField()
    fullname = serializers.CharField()
    username = serializers.CharField(allow_null=True)
    is_premium = serializers.BooleanField()
    can_be_added_to_contacts = serializers.BooleanField()
    secret_message_theme = SecretMessageThemeSerializer()
    profile_photo_url = serializers.URLField(allow_null=True)
    is_banned = serializers.BooleanField()
    can_receive_notifications = serializers.BooleanField()
    born_at = serializers.DateField(allow_null=True)


class UserRetrieveUpdateApi(APIView):

    class InputSerializer(serializers.Serializer):
        fullname = serializers.CharField()
        username = serializers.CharField(allow_null=True)
        can_be_added_to_contacts = serializers.BooleanField()
        secret_message_theme_id = serializers.IntegerField(allow_null=True)
        can_receive_notifications = serializers.BooleanField()
        born_at = serializers.DateField(allow_null=True)

    def get(self, request: Request, user_id: int):
        try:
            user = get_user_by_id(user_id)
        except UserDoesNotExistsError:
            raise NotFound('User does not exist')
        serializer = UserOutputSerializer(user)
        return Response(serializer.data)

    def put(self, request: Request, user_id: int):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        fullname: str = serialized_data['fullname']
        username: str | None = serialized_data['username']
        can_be_added_to_contacts: bool = (
            serialized_data['can_be_added_to_contacts']
        )
        secret_message_theme_id: int | None = (
            serialized_data['secret_message_theme_id']
        )
        can_receive_notifications: bool = (
            serialized_data['can_receive_notifications']
        )
        born_at: date | None = serialized_data['born_at']

        is_updated = update_user(
            user_id=user_id,
            fullname=fullname,
            username=username,
            can_be_added_to_contacts=can_be_added_to_contacts,
            secret_message_theme_id=secret_message_theme_id,
            can_receive_notifications=can_receive_notifications,
            born_at=born_at,
        )

        response_status_code = (
            status.HTTP_204_NO_CONTENT
            if is_updated else status.HTTP_404_NOT_FOUND
        )
        return Response(status=response_status_code)


class UserCreateApi(APIView):

    class InputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        fullname = serializers.CharField(max_length=64)
        username = serializers.CharField(max_length=64, allow_null=True)

    def post(self, request: Request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        user_id: int = serialized_data['id']
        fullname: str = serialized_data['fullname']
        username: str | None = serialized_data['username']

        try:
            user = create_user(
                user_id=user_id,
                fullname=fullname,
                username=username,
            )
        except UserAlreadyExistsError:
            error = APIException('User already exists')
            error.status_code = status.HTTP_409_CONFLICT
            raise error

        serializer = UserOutputSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
