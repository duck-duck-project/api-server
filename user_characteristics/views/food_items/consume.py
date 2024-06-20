from rest_framework import serializers, status
from rest_framework.exceptions import APIException
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from economics.exceptions import InsufficientFundsForSystemWithdrawalError
from user_characteristics.exceptions import FoodItemDoesNotExistError
from user_characteristics.selectors.food_items import get_food_item_by_name
from user_characteristics.services.food_items import consume_food_item
from users.exceptions import NotEnoughHealthError
from users.services.users import get_or_create_user

__all__ = ('FoodItemConsumeApi',)


class FoodItemConsumeApi(APIView):
    class InputSerializer(serializers.Serializer):
        user_id = serializers.IntegerField()
        food_item_name = serializers.CharField(max_length=64)

    class OutputSerializer(serializers.Serializer):
        user_id = serializers.IntegerField()
        food_item_name = serializers.CharField()
        food_item_emoji = serializers.CharField(allow_null=True)
        price = serializers.IntegerField()
        energy_benefit_value = serializers.IntegerField()
        user_energy = serializers.IntegerField()
        health_impact_value = serializers.IntegerField()
        user_health = serializers.IntegerField()

    def post(self, request: Request) -> Response:
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        user_id: int = serialized_data['user_id']
        food_item_name: str = serialized_data['food_item_name']

        user, _ = get_or_create_user(user_id)

        try:
            food_item = get_food_item_by_name(food_item_name)
        except FoodItemDoesNotExistError as error:
            api_error = APIException({
                'detail': 'Food item does not exist',
                'food_item_name': error.food_item_name,
            })
            api_error.status_code = status.HTTP_404_NOT_FOUND
            raise api_error

        try:
            consumption_result = consume_food_item(
                user=user,
                food_item=food_item,
            )
        except InsufficientFundsForSystemWithdrawalError as error:
            api_error = APIException({
                'detail': 'Not enough balance to buy food item',
                'price': error.amount,
                'food_item_name': food_item_name,
            })
            raise api_error
        except NotEnoughHealthError as error:
            api_error = APIException({
                'detail': 'Not enough health to consume food item',
                'required_health_value': error.cost,
                'food_item_name': food_item_name,
            })
            raise api_error

        serializer = self.OutputSerializer(consumption_result)
        response_data = {'ok': True, 'result': serializer.data}
        return Response(response_data)
