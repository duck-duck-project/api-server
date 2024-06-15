from rest_framework import serializers, status
from rest_framework.exceptions import APIException
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from mining.exceptions import MiningActionThrottledError
from mining.services import create_mining_action, get_mining_statistics
from users.services.users import get_or_create_user

__all__ = ('MiningActionCreateApi', 'MiningUserStatisticsApi')


class MiningActionCreateApi(APIView):
    class InputSerializer(serializers.Serializer):
        user_id = serializers.IntegerField()

    class OutputSerializer(serializers.Serializer):
        user_id = serializers.IntegerField()
        resource_name = serializers.CharField()
        wealth = serializers.IntegerField()
        next_mining_at = serializers.DateTimeField()

    def post(self, request: Request) -> Response:
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data
        user_id: int = serialized_data['user_id']

        user, _ = get_or_create_user(user_id=user_id)
        try:
            mining_action = create_mining_action(user=user)
        except MiningActionThrottledError as error:
            error = APIException({
                'detail': str(error),
                'next_mining_in_seconds': error.next_mining_in_seconds,
            })
            error.status_code = status.HTTP_400_BAD_REQUEST
            raise error

        serializer = self.OutputSerializer(mining_action)
        response_data = {'ok': True, 'result': serializer.data}
        return Response(response_data, status=status.HTTP_201_CREATED)


class MiningUserStatisticsApi(APIView):

    class InputSerializer(serializers.Serializer):
        user_id = serializers.IntegerField()

    class OutputSerializer(serializers.Serializer):
        class ResourceSerializer(serializers.Serializer):
            name = serializers.CharField()
            total_wealth = serializers.IntegerField()
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
        response_data = {'ok': True, 'result': serializer.data}
        return Response(response_data)
