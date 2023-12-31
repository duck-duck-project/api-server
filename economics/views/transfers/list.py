from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from economics.models import Transaction
from economics.selectors import get_latest_user_transactions
from users.serializers import UserPartialSerializer

__all__ = ('TransactionListApi',)


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
