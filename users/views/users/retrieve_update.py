from rest_framework import serializers, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from users.selectors.users import get_user_by_id
from users.serializers import UserSerializer
from users.services.users import update_user

__all__ = ('UserRetrieveUpdateApi',)


class UserRetrieveUpdateApi(APIView):

    class InputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        can_be_added_to_contacts = serializers.BooleanField()
        theme_id = serializers.UUIDField(allow_null=True)
        can_receive_notifications = serializers.BooleanField()
        profile_photo_url = serializers.URLField()
        born_on = serializers.DateField()
        personality_type_prefix = serializers.ChoiceField(
            choices=User.PersonalityTypePrefix.choices,
        )
        personality_type_suffix = serializers.ChoiceField(
            choices=User.PersonalityTypeSuffix.choices,
        )
        real_first_name = serializers.CharField(max_length=64, required=False)
        real_last_name = serializers.CharField(max_length=64, required=False)
        patronymic = serializers.CharField(max_length=64, required=False)
        gender = serializers.ChoiceField(
            choices=User.Gender.choices,
            required=False,
        )
        is_from_private_chat = serializers.BooleanField(default=False)

    def get(self, request: Request, user_id: int) -> Response:
        user = get_user_by_id(user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request: Request, user_id: int) -> Response:
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        update_user(
            user_id=user_id,
            **serialized_data,
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
