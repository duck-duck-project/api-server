from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from holidays.selectors import get_date_holidays

__all__ = ('HolidaysApi',)


class HolidaysApi(APIView):
    class InputSerializer(serializers.Serializer):
        day = serializers.IntegerField(min_value=1, max_value=31)
        month = serializers.IntegerField(min_value=1, max_value=12)

    class OutputSerializer(serializers.Serializer):
        day = serializers.IntegerField()
        month = serializers.IntegerField()
        holidays = serializers.ListField(child=serializers.CharField())

    def get(self, request: Request) -> Response:
        serializer = self.InputSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        day: int = serialized_data['day']
        month: int = serialized_data['month']

        date_holidays = get_date_holidays(month=month, day=day)
        serializer = self.OutputSerializer(date_holidays)
        return Response({'ok': True, 'result': serializer.data})
