from rest_framework import serializers, status
from rest_framework.exceptions import APIException
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from user_characteristics.exceptions import (
    SportActivityCooldownError,
    SportActivityDoesNotExistError,
)
from user_characteristics.selectors.sport_activities import (
    get_sport_activity_by_name,
)
from user_characteristics.services.sport_activity_actions.domain import (
    create_sport_activity_action,
)
from users.exceptions import NotEnoughEnergyError
from users.services.users import get_or_create_user

__all__ = ('SportActivityActionCreateApi',)


class SportActivityActionCreateApi(APIView):
    class InputSerializer(serializers.Serializer):
        user_id = serializers.IntegerField()
        sport_activity_name = serializers.CharField(max_length=64)

    class OutputSerializer(serializers.Serializer):
        user_id = serializers.IntegerField()
        user_energy = serializers.IntegerField()
        user_health = serializers.IntegerField()
        energy_cost_value = serializers.IntegerField()
        sport_activity_name = serializers.CharField()
        health_benefit_value = serializers.IntegerField()
        cooldown_in_seconds = serializers.IntegerField()

    def post(self, request: Request) -> Response:
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.validated_data

        user_id: int = serialized_data['user_id']
        sport_activity_name: str = serialized_data['sport_activity_name']

        user, _ = get_or_create_user(user_id)

        try:
            sport_activity = get_sport_activity_by_name(sport_activity_name)
        except SportActivityDoesNotExistError as error:
            error = APIException({
                'detail': 'Sport activity does not exist',
                'sport_activity_name': error.sport_activity_name,
            })
            error.status_code = status.HTTP_404_NOT_FOUND
            raise error

        try:
            sport_activity_action_result = create_sport_activity_action(
                user=user,
                sport_activity=sport_activity,
            )
        except SportActivityCooldownError as error:
            api_error = APIException({
                'detail': 'Sport activity is on cooldown',
                'sport_activity_name': sport_activity_name,
                'cooldown_in_seconds': error.cooldown_in_seconds,
                'next_activity_in_seconds': error.next_activity_in_seconds,
            })
            api_error.status_code = status.HTTP_400_BAD_REQUEST
            raise api_error
        except NotEnoughEnergyError as error:
            api_error = APIException({
                'detail': 'Not enough energy',
                'required_energy_value': error.cost,
            })
            api_error.status_code = status.HTTP_400_BAD_REQUEST
            raise api_error

        serializer = self.OutputSerializer(sport_activity_action_result)
        response_data = {'ok': True, 'result': serializer.data}
        return Response(response_data, status=status.HTTP_201_CREATED)
