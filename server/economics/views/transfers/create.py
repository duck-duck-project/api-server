from rest_framework import serializers, status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from economics.exceptions import InsufficientFundsForTransferError
from economics.models import Transaction
from economics.services import create_transfer
from users.exceptions import UserDoesNotExistsError
from users.selectors.users import get_user_by_id
from users.serializers import UserPartialSerializer

__all__ = ('TransferCreateApi',)


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
