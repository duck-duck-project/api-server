from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from economics.exceptions import InsufficientFundsForTransferError
from economics.models import Transaction
from economics.selectors import get_latest_user_transactions
from economics.services import create_transfer, compute_user_balance
from users.exceptions import UserDoesNotExistsError
from users.selectors.users import get_user_by_id

__all__ = ('TransferCreateApi', 'TransactionListApi', 'BalanceRetrieveApi')


class UserPartialSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    fullname = serializers.CharField()


class TransactionListApi(APIView):

    class InputSerializer(serializers.Serializer):
        limit = serializers.IntegerField(default=10, max_value=50)
        offset = serializers.IntegerField(default=0)

    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        sender = UserPartialSerializer(allow_null=True)
        recipient = UserPartialSerializer(allow_null=True)
        amount = serializers.IntegerField()
        description = serializers.CharField(max_length=255, allow_null=True)
        source = serializers.ChoiceField(choices=Transaction.Source.choices)
        created_at = serializers.DateTimeField()

    def get(self, request: Request, user_id: int):
        serializer = self.InputSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.validated_data

        limit: int = serialized_data['limit']
        offset: int = serialized_data['offset']

        transactions = get_latest_user_transactions(
            user_id=user_id,
            limit=limit + 1,
            offset=offset,
        )
        is_end_of_list_reached = len(transactions) <= limit
        transactions = transactions[:limit]

        serializer = self.OutputSerializer(transactions, many=True)
        response_data = {
            'transactions': serializer.data,
            'is_end_of_list_reached': is_end_of_list_reached,
        }
        return Response(response_data)


class TransferCreateApi(APIView):

    class InputSerializer(serializers.Serializer):
        sender_id = serializers.IntegerField()
        recipient_id = serializers.IntegerField()
        amount = serializers.IntegerField(
            min_value=1,
            max_value=5000,
            error_messages={
                'min_value': 'Amount must be greater than 0',
                'max_value': 'Amount must be less or equal to 5000',
            }
        )
        description = serializers.CharField(max_length=255, allow_null=True)

    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        sender = UserPartialSerializer()
        recipient = UserPartialSerializer()
        amount = serializers.IntegerField()
        description = serializers.CharField(max_length=255, allow_null=True)
        source = serializers.ChoiceField(choices=Transaction.Source.choices)
        created_at = serializers.DateTimeField()

    def post(self, request: Request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.validated_data

        sender_id: int = serialized_data['sender_id']
        recipient_id: int = serialized_data['recipient_id']
        amount: int = serialized_data['amount']
        description: str | None = serialized_data['description']

        try:
            sender = get_user_by_id(sender_id)
            recipient = get_user_by_id(recipient_id)
        except UserDoesNotExistsError:
            raise NotFound('User does not exists')

        try:
            transfer = create_transfer(
                sender=sender,
                recipient=recipient,
                amount=amount,
                description=description,
            )
        except InsufficientFundsForTransferError:
            raise ValidationError('Insufficient funds for transfer')

        serializer = self.OutputSerializer(transfer)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


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
