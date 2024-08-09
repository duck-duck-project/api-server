from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

__all__ = ('RelationCreateApi',)


class RelationCreateApi(APIView):
    class InputSerializer(serializers.Serializer):
        user_ids = serializers.ListField(
            child=serializers.IntegerField(),
            min_length=2,
            max_length=2,
            allow_empty=False,
        )

        def validate_user_ids(self, value: list[int]) -> list[int]:
            if value[0] == value[1]:
                raise serializers.ValidationError('User ids must be different')
            return value

    class OutputSerializer(serializers.Serializer):
        pass

    def post(self, request: Request) -> Response:
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data: dict = serializer.validated_data

        user_ids: list[int] = serialized_data['user_ids']



        response_data = {'ok': True}
        return Response(response_data)
