from rest_framework import serializers, status
from rest_framework.exceptions import NotFound
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from users.exceptions import UserDoesNotExistsError
from users.selectors.users import get_user_by_id
from users.serializers import UserSerializer
from users.services.users import upsert_user

__all__ = (
    'UserRetrieveApi',
    'UserCreateUpdateApi',
)


class UserRetrieveApi(APIView):
    OutputSerializer = UserSerializer

    def get(self, request: Request, user_id: int):
        try:
            user = get_user_by_id(user_id)
        except UserDoesNotExistsError:
            raise NotFound('User does not exist')
        serializer = self.OutputSerializer(user)
        return Response(serializer.data)


class UserCreateUpdateApi(APIView):
    OutputSerializer = UserSerializer

    class InputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        fullname = serializers.CharField()
        username = serializers.CharField(allow_null=True)
        can_be_added_to_contacts = serializers.BooleanField(required=False)
        theme_id = serializers.UUIDField(required=False)
        can_receive_notifications = serializers.BooleanField(required=False)
        profile_photo_url = serializers.URLField(required=False)
        is_from_private_chat = serializers.BooleanField(default=None)

    def post(self, request: Request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        user_id: int = serialized_data.pop('id')
        is_from_private_chat: bool | None = (
            serialized_data.pop('is_from_private_chat')
        )
        if is_from_private_chat:
            serialized_data['is_blocked_bot'] = False

        user, is_created = upsert_user(
            user_id=user_id,
            defaults=serialized_data,
        )

        serializer = self.OutputSerializer(user)
        response_data = {'ok': True, 'result': serializer.data}
        status_code = (
            status.HTTP_201_CREATED
            if is_created else status.HTTP_200_OK
        )
        return Response(response_data, status=status_code)
