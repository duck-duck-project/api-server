from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from user_characteristics.models import FoodItem
from user_characteristics.selectors.food_items import get_food_items

__all__ = ('FoodItemListApi',)


class FoodItemListApi(APIView):
    class OutputSerializer(serializers.Serializer):
        name = serializers.CharField()
        emoji = serializers.CharField(allow_null=True)
        type = serializers.ChoiceField(choices=FoodItem.Type.choices)
        price = serializers.IntegerField()
        energy_benefit_value = serializers.IntegerField()
        health_impact_value = serializers.IntegerField()

    def get(self, request: Request) -> Response:
        food_items = get_food_items()
        serializer = self.OutputSerializer(food_items, many=True)
        response_data = {'ok': True, 'result': serializer.data}
        return Response(response_data)
