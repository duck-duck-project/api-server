from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from economics.exceptions import InsufficientFundsForSystemWithdrawalError
from economics.serializers import (
    SystemTransactionInputSerializer,
    SystemTransactionOutputSerializer,
)
from economics.services import create_system_withdrawal
from users.exceptions import UserDoesNotExistsError
from users.selectors.users import get_user_by_id
from users.serializers import UserPartialSerializer

__all__ = ('SystemWithdrawalCreateApi',)


class SystemWithdrawalCreateApi(APIView):

    InputSerializer = SystemTransactionInputSerializer

    class OutputSerializer(SystemTransactionOutputSerializer):
        user = UserPartialSerializer(source='sender')

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

        try:
            withdrawal = create_system_withdrawal(
                user=user,
                amount=amount,
                description=description,
            )
        except InsufficientFundsForSystemWithdrawalError:
            raise ValidationError('Insufficient funds for withdrawal')

        serializer = self.OutputSerializer(withdrawal)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
