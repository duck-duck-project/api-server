from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from user_characteristics.selectors.medicines import get_medicines

__all__ = ('MedicineListApi',)


class MedicineListApi(APIView):
    class OutputSerializer(serializers.Serializer):
        name = serializers.CharField()
        emoji = serializers.CharField(allow_null=True)
        health_benefit_value = serializers.IntegerField()
        price = serializers.IntegerField()

    def get(self, request: Request) -> Response:
        medicines = get_medicines()
        serializer = self.OutputSerializer(medicines, many=True)
        response_data = {'ok': True, 'result': serializer.data}
        return Response(response_data)
