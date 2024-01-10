from uuid import UUID

from rest_framework import serializers, status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from economics.exceptions import (
    InsufficientFundsForTransferError,
    TransactionDoesNotExistError,
    TransactionIsNotTransferError,
    TransferSenderDoesNotMatchError, TransferRollbackTimeExpiredError,
    InsufficientFundsForTransferRollbackError,
)
from economics.selectors import get_transaction_by_id
from economics.services import create_transfer, rollback_transfer
from users.exceptions import UserDoesNotExistsError
from users.selectors.users import get_user_by_id
from users.serializers import UserPartialSerializer

__all__ = ('TransferCreateDeleteApi',)


class TransferCreateDeleteApi(APIView):

    class InputDeleteSerializer(serializers.Serializer):
        user_id = serializers.IntegerField()
        transaction_id = serializers.UUIDField()

    class InputCreateSerializer(serializers.Serializer):
        sender_id = serializers.IntegerField()
        recipient_id = serializers.IntegerField()
        amount = serializers.IntegerField(
            min_value=1,
            error_messages={
                'min_value': 'Amount must be greater than 0',
            }
        )
        description = serializers.CharField(max_length=255, allow_null=True)

    class OutputCreateSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        sender = UserPartialSerializer()
        recipient = UserPartialSerializer()
        amount = serializers.IntegerField()
        description = serializers.CharField(max_length=255, allow_null=True)
        created_at = serializers.DateTimeField()

    def post(self, request: Request):
        serializer = self.InputCreateSerializer(data=request.data)
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

        serializer = self.OutputCreateSerializer(transfer)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request: Request):
        """
        Delete transfer by id.
        Only transfer sender can delete transaction.
        """
        serializer = self.InputDeleteSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        serialized_data = serializer.data
        user_id: int = serialized_data['user_id']
        transaction_id: UUID = serialized_data['transaction_id']

        try:
            transaction = get_transaction_by_id(transaction_id)
        except TransactionDoesNotExistError:
            raise NotFound(detail='Transaction does not exist')

        try:
            rollback_transfer(
                transaction=transaction,
                user_id=user_id,
            )
        except (
                TransferSenderDoesNotMatchError,
                TransactionIsNotTransferError,
                TransferRollbackTimeExpiredError,
                InsufficientFundsForTransferRollbackError,
        ) as error:
            raise ValidationError(detail=str(error))

        return Response(status=status.HTTP_204_NO_CONTENT)
