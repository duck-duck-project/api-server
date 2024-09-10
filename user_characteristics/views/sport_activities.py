from rest_framework import serializers, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from user_characteristics.selectors.sport_activities import (
    get_sport_activities,
    get_sport_activity_by_name,
)
from user_characteristics.services.sport_activity_actions.domain import (
    create_sport_activity_action,
)
from users.services.users import get_or_create_user

__all__ = ('SportActivityListCreateApi',)


class SportActivityListCreateApi(APIView):

    class InputCreateSerializer(serializers.Serializer):
        user_id = serializers.IntegerField()
        sport_activity_name = serializers.CharField(max_length=64)

    class OutputCreateSerializer(serializers.Serializer):
        user_id = serializers.IntegerField()
        user_energy = serializers.IntegerField()
        user_health = serializers.IntegerField()
        energy_cost_value = serializers.IntegerField()
        sport_activity_name = serializers.CharField()
        health_benefit_value = serializers.IntegerField()
        cooldown_in_seconds = serializers.IntegerField()

    class OutputListSerializer(serializers.Serializer):
        name = serializers.CharField()
        emoji = serializers.CharField(allow_null=True)
        energy_cost_value = serializers.IntegerField()
        health_benefit_value = serializers.IntegerField()
        cooldown_in_seconds = serializers.IntegerField()

    def get(self, request: Request) -> Response:
        sport_activities = get_sport_activities()
        serializer = self.OutputListSerializer(sport_activities, many=True)
        response_data = {'sport_activities': serializer.data}
        return Response(response_data)

    def post(self, request: Request) -> Response:
        serializer = self.InputCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.validated_data

        user_id: int = serialized_data['user_id']
        sport_activity_name: str = serialized_data['sport_activity_name']

        user, _ = get_or_create_user(user_id)

        sport_activity = get_sport_activity_by_name(sport_activity_name)

        sport_activity_action_result = create_sport_activity_action(
            user=user,
            sport_activity=sport_activity,
        )

        serializer = self.OutputCreateSerializer(sport_activity_action_result)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
