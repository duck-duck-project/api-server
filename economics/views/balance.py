from rest_framework import serializers, status
from rest_framework.exceptions import NotFound
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from economics.services import compute_user_balance
from economics.tasks import send_richest_users
from users.exceptions import UserDoesNotExistsError
from users.selectors.users import get_user_by_id

__all__ = ('BalanceRetrieveApi', 'RichestUsersStatisticsApi')


class BalanceRetrieveApi(APIView):

    def get(self, request: Request, user_id: int):
        try:
            user = get_user_by_id(user_id)
        except UserDoesNotExistsError:
            raise NotFound('User does not exists')
        balance = compute_user_balance(user)
        response_data = {
            'user_id': user.id,
            'balance': balance,
        }
        return Response(response_data)


class RichestUsersStatisticsApi(APIView):

    class InputSerializer(serializers.Serializer):
        limit = serializers.IntegerField(required=False, default=10)
        chat_id = serializers.IntegerField()
        user_id = serializers.IntegerField()

    def post(self, request: Request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        limit: int | None = serialized_data['limit']
        chat_id: int = serialized_data['chat_id']
        user_id: int = serialized_data['user_id']

        send_richest_users.delay(
            called_by_user_id=user_id,
            chat_id=chat_id,
            limit=limit,
        )
        return Response(status=status.HTTP_202_ACCEPTED)
