from rest_framework import serializers, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import UserSerializer
from users.services.users import upsert_user

__all__ = ('UserCreateApi',)


class UserCreateApi(APIView):

    class InputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        fullname = serializers.CharField(max_length=64, default='Anonymous')
        username = serializers.CharField(
            max_length=64,
            allow_null=True,
            default=None,
        )

    def post(self, request: Request) -> Response:
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        user, _ = upsert_user(
            user_id=serialized_data.pop('id'),
            defaults=serialized_data
        )

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
