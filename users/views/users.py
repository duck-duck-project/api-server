from rest_framework import serializers, status
from rest_framework.exceptions import NotFound
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from users.exceptions import UserDoesNotExistsError
from users.selectors.users import get_user_by_id
from users.services.users import upsert_user

__all__ = (
    'UserRetrieveApi',
    'UserCreateUpdateApi',
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
    can_be_added_to_contacts = serializers.BooleanField()
    secret_message_theme = SecretMessageThemeSerializer()
    profile_photo_url = serializers.URLField(allow_null=True)
    is_banned = serializers.BooleanField()
    can_receive_notifications = serializers.BooleanField()


class UserRetrieveApi(APIView):

    def get(self, request: Request, user_id: int):
        try:
            user = get_user_by_id(user_id)
        except UserDoesNotExistsError:
            raise NotFound('User does not exist')
        serializer = UserOutputSerializer(user)
        return Response(serializer.data)


class UserCreateUpdateApi(APIView):
    class InputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        fullname = serializers.CharField()
        username = serializers.CharField(allow_null=True)
        can_be_added_to_contacts = serializers.BooleanField(required=False)
        secret_message_theme_id = serializers.IntegerField(
            allow_null=True,
            required=False,
        )
        can_receive_notifications = serializers.BooleanField(required=False)
        profile_photo_url = serializers.URLField(
            allow_null=True,
            required=False,
        )

    def post(self, request: Request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        user_id: int = serialized_data.pop('id')

        user, is_created = upsert_user(
            user_id=user_id,
            defaults=serialized_data,
        )

        serializer = UserOutputSerializer(user)
        response_data = {'ok': True, 'result': serializer.data}
        status_code = (
            status.HTTP_201_CREATED
            if is_created else status.HTTP_200_OK
        )
        return Response(response_data, status=status_code)
