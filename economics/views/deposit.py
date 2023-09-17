from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from economics.serializers import (
    SystemTransactionInputSerializer,
    SystemTransactionOutputSerializer,
)
from economics.services import create_system_deposit
from users.exceptions import UserDoesNotExistsError
from users.selectors.users import get_user_by_id
from users.serializers import UserPartialSerializer

__all__ = ('SystemDepositCreateApi',)


class SystemDepositCreateApi(APIView):

    InputSerializer = SystemTransactionInputSerializer

    class OutputSerializer(SystemTransactionOutputSerializer):
        user = UserPartialSerializer(source='recipient')

    def post(self, request: Request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        user_id: int = serialized_data['user_id']
        amount: int = serialized_data['amount']
        description: str = serialized_data['description']

        try:
            user = get_user_by_id(user_id)
        except UserDoesNotExistsError:
            raise NotFound('User does not exists')

        deposit = create_system_deposit(
            user=user,
            amount=amount,
            description=description,
        )

        serializer = self.OutputSerializer(deposit)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
