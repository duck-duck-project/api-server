from rest_framework import serializers

from economics.models import Transaction
from users.serializers import UserPartialSerializer

__all__ = (
    'SystemTransactionInputSerializer',
    'SystemTransactionOutputSerializer',
)


class SystemTransactionInputSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    amount = serializers.IntegerField(
        min_value=1,
        error_messages={
            'min_value': 'Amount must be greater than 0',
        },
    )
    description = serializers.CharField(max_length=255)


class SystemTransactionOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    user = UserPartialSerializer()
    amount = serializers.IntegerField()
    description = serializers.CharField(max_length=255, allow_null=True)
    created_at = serializers.DateTimeField()
