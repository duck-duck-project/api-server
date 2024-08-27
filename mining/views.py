from rest_framework import serializers, status
from rest_framework.exceptions import APIException
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from mining.services.mining_actions import create_mining_action
from mining.services.statistics import get_mining_statistics
from users.services.users import get_or_create_user

__all__ = ('MiningActionCreateApi', 'MiningUserStatisticsApi')


class MiningActionCreateApi(APIView):
    class InputSerializer(serializers.Serializer):
        user_id = serializers.IntegerField()
        chat_id = serializers.IntegerField(default=None)

    class OutputSerializer(serializers.Serializer):
        user_id = serializers.IntegerField()
        chat_id = serializers.IntegerField()
        resource_name = serializers.CharField()
        value = serializers.IntegerField()
        value_per_gram = serializers.FloatField()
        weight_in_grams = serializers.IntegerField()
        spent_energy = serializers.IntegerField()
        remaining_energy = serializers.IntegerField()

    def post(self, request: Request) -> Response:
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        user_id: int = serialized_data['user_id']
        chat_id: int | None = serialized_data['chat_id']

        user, _ = get_or_create_user(user_id=user_id)
        mining_action = create_mining_action(user=user, chat_id=chat_id)

        serializer = self.OutputSerializer(mining_action)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MiningUserStatisticsApi(APIView):
    class InputSerializer(serializers.Serializer):
        user_id = serializers.IntegerField()

    class OutputSerializer(serializers.Serializer):
        class ResourceSerializer(serializers.Serializer):
            name = serializers.CharField()
            total_value = serializers.IntegerField()
            total_count = serializers.IntegerField()

        user_id = serializers.IntegerField()
        resources = ResourceSerializer(many=True)

    def get(self, request: Request) -> Response:
        serializer = self.InputSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        user_id: int = serialized_data['user_id']

        mining_statistics = get_mining_statistics(user_id=user_id)

        serializer = self.OutputSerializer(mining_statistics)
        return Response(serializer.data)
