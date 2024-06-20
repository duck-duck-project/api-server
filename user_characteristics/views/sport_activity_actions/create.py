from rest_framework import serializers, status
from rest_framework.exceptions import APIException
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from user_characteristics.exceptions import SportActivityDoesNotExistError
from user_characteristics.selectors.sport_activities import (
    get_sport_activity_by_name
)
from users.services.users import get_or_create_user

__all__ = ('SportActivityActionCreateApi',)


class SportActivityActionCreateApi(APIView):
    class InputSerializer(serializers.Serializer):
        user_id = serializers.IntegerField()
        sport_activity_name = serializers.CharField(max_length=64)

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

        return Response()
