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
        theme_id = serializers.UUIDField(allow_null=True)
        can_receive_notifications = serializers.BooleanField(required=False)
        can_be_added_to_contacts = serializers.BooleanField(required=False)
        profile_photo_url = serializers.URLField(allow_null=True)
        born_on = serializers.DateField(allow_null=True)
        personality_type_prefix = serializers.ChoiceField(
            choices=User.PersonalityTypePrefix.choices,
            allow_null=True,
            required=False,
        )
        personality_type_suffix = serializers.ChoiceField(
            choices=User.PersonalityTypeSuffix.choices,
            allow_null=True,
            required=False,
        )
        real_first_name = serializers.CharField(max_length=64, allow_null=True)
        real_last_name = serializers.CharField(max_length=64, allow_null=True)
        patronymic = serializers.CharField(max_length=64, allow_null=True)
        gender = serializers.ChoiceField(
            choices=User.Gender.choices,
            allow_null=True,
        )

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
