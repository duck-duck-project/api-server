from rest_framework import serializers, status
from rest_framework.exceptions import APIException
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from economics.exceptions import InsufficientFundsForSystemWithdrawalError
from user_characteristics.exceptions import MedicineNotFoundError
from user_characteristics.selectors.medicines import get_medicine_by_name
from user_characteristics.services.medicines import consume_medicine
from users.services.users import get_or_create_user

__all__ = ('MedicineConsumeApi',)


class MedicineConsumeApi(APIView):
    class InputSerializer(serializers.Serializer):
        user_id = serializers.IntegerField()
        medicine_name = serializers.CharField(max_length=64)

    class OutputSerializer(serializers.Serializer):
        user_id = serializers.IntegerField()
        medicine_name = serializers.CharField()
        price = serializers.IntegerField()
        health_benefit_value = serializers.IntegerField()
        user_health = serializers.IntegerField()

    def post(self, request: Request) -> Response:
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        user_id: int = serialized_data['user_id']
        medicine_name: str = serialized_data['medicine_name']

        user, _ = get_or_create_user(user_id)

        medicine = get_medicine_by_name(medicine_name)

        consumption_result = consume_medicine(user=user, medicine=medicine)

        serializer = self.OutputSerializer(consumption_result)
        return Response(serializer.data)
