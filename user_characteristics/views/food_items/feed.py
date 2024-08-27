from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from user_characteristics.models import FoodItem
from user_characteristics.selectors.food_items import \
    get_food_item_by_name_and_type
from user_characteristics.services.food_items import feed_user
from users.services.users import get_or_create_user

__all__ = ('FoodItemFeedApi',)


class FoodItemFeedApi(APIView):
    class InputSerializer(serializers.Serializer):
        from_user_id = serializers.IntegerField()
        to_user_id = serializers.IntegerField()
        food_item_name = serializers.CharField(max_length=64)
        food_item_type = serializers.ChoiceField(choices=FoodItem.Type.choices)

    class OutputSerializer(serializers.Serializer):
        from_user_id = serializers.IntegerField()
        to_user_id = serializers.IntegerField()
        food_item_name = serializers.CharField()
        food_item_type = serializers.ChoiceField(choices=FoodItem.Type.choices)
        food_item_emoji = serializers.CharField(allow_null=True)
        price = serializers.IntegerField()
        energy_benefit_value = serializers.IntegerField()
        health_impact_value = serializers.IntegerField()
        user_energy = serializers.IntegerField()
        user_health = serializers.IntegerField()

    def post(self, request: Request) -> Response:
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        from_user_id: int = serialized_data['from_user_id']
        to_user_id: int = serialized_data['to_user_id']
        food_item_name: str = serialized_data['food_item_name']
        food_item_type: int = serialized_data['food_item_type']

        from_user, _ = get_or_create_user(from_user_id)
        to_user, _ = get_or_create_user(to_user_id)

        food_item = get_food_item_by_name_and_type(
            food_item_name=food_item_name,
            food_item_type=food_item_type,
        )

        user_feed_result = feed_user(
            from_user=from_user,
            to_user=to_user,
            food_item=food_item,
        )

        serializer = self.OutputSerializer(user_feed_result)
        response_data = {'ok': True, 'result': serializer.data}
        return Response(response_data)
