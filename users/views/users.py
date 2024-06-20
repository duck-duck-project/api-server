from rest_framework import serializers, status
from rest_framework.exceptions import APIException, NotFound
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from users.exceptions import (
    NotEnoughEnergyError, NotEnoughHealthError, UserDoesNotExistsError,
    UserSportsThrottledError,
)
from users.models import User
from users.selectors.users import get_user_by_id
from users.serializers import UserSerializer
from users.services.users import (
    consume_food, do_sport_activity,
    get_or_create_user,
    increase_user_energy,
    upsert_user,
)

__all__ = (
    'UserRetrieveApi',
    'UserCreateUpdateApi',
    'UserFoodConsumeApi',
    'UserDoSportsApi',
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
        born_on = serializers.DateField(required=False)
        personality_type_prefix = serializers.ChoiceField(
            choices=User.PersonalityTypePrefix.choices,
            required=False,
        )
        personality_type_suffix = serializers.ChoiceField(
            choices=User.PersonalityTypeSuffix.choices,
            required=False,
        )
        real_first_name = serializers.CharField(max_length=64, required=False)
        real_last_name = serializers.CharField(max_length=64, required=False)
        patronymic = serializers.CharField(max_length=64, required=False)
        gender = serializers.ChoiceField(
            choices=User.Gender.choices,
            required=False,
        )
        contacts_sorting_strategy = serializers.ChoiceField(
            choices=User.ContactsSortingStrategy.choices,
            required=False,
        )
        is_contacts_sorting_reversed = serializers.BooleanField(required=False)

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


class UserFoodConsumeApi(APIView):
    class InputSerializer(serializers.Serializer):
        user_id = serializers.IntegerField()
        energy = serializers.IntegerField(min_value=1, max_value=10000)
        health_impact_value = serializers.IntegerField()

    class OutputSerializer(serializers.Serializer):
        user_id = serializers.IntegerField(source='id')
        energy = serializers.IntegerField()

    def post(self, request: Request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        user_id: int = serialized_data['user_id']
        energy: int = serialized_data['energy']
        health_impact_value: int = serialized_data['health_impact_value']

        user, _ = get_or_create_user(user_id=user_id)

        try:
            consume_food(user, health_impact_value=health_impact_value)
        except NotEnoughHealthError as error:
            error = APIException({
                'detail': str(error),
                'required_health': error.cost,
            })
            error.status_code = status.HTTP_400_BAD_REQUEST
            raise error

        serializer = self.OutputSerializer(user)
        response_data = {'ok': True, 'result': serializer.data}
        return Response(response_data)


class UserDoSportsApi(APIView):
    class InputSerializer(serializers.Serializer):
        user_id = serializers.IntegerField()
        health_benefit_value = serializers.IntegerField(
            min_value=1,
            max_value=10000,
        )
        energy_cost_value = serializers.IntegerField(
            min_value=1,
            max_value=10000,
        )

    class OutputSerializer(serializers.Serializer):
        user_id = serializers.IntegerField(source='id')
        health = serializers.IntegerField()

    def post(self, request: Request) -> Response:
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        user_id: int = serialized_data['user_id']
        energy_cost_value: int = serialized_data['energy_cost_value']
        health_benefit_value: int = serialized_data['health_benefit_value']

        user, _ = get_or_create_user(user_id=user_id)

        try:
            user = do_sport_activity(
                user=user,
                health_benefit_value=health_benefit_value,
                energy_cost_value=energy_cost_value,
            )
        except NotEnoughEnergyError as error:
            error = APIException({
                'detail': str(error),
                'required_energy': error.cost,
            })
            error.status_code = status.HTTP_400_BAD_REQUEST
            raise error
        except UserSportsThrottledError as error:
            error = APIException(
                detail={
                    'detail': str(error),
                    'next_sports_in_seconds': error.next_sports_in_seconds,
                },
            )
            error.status_code = status.HTTP_400_BAD_REQUEST
            raise error

        serializer = self.OutputSerializer(user)
        response_data = {'ok': True, 'result': serializer.data}
        return Response(response_data)
