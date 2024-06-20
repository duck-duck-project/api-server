from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from user_characteristics.selectors.sport_activities import get_sport_activities

__all__ = ('SportActivityListApi',)


class SportActivityListApi(APIView):
    class OutputSerializer(serializers.Serializer):
        name = serializers.CharField()
        emoji = serializers.CharField(allow_null=True)
        energy_cost_value = serializers.IntegerField()
        health_benefit_value = serializers.IntegerField()
        cooldown_in_seconds = serializers.IntegerField()

    def get(self, request: Request) -> Response:
        sport_activities = get_sport_activities()
        serializer = self.OutputSerializer(sport_activities, many=True)
        response_data = {'ok': True, 'result': serializer.data}
        return Response(response_data)
