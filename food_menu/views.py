from rest_framework import serializers
from rest_framework.exceptions import APIException
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from food_menu.exceptions import FoodMenuParseError, FoodMenuApiRequestError
from food_menu.services import get_food_menu_html, parse_food_menu_html

__all__ = ('FoodMenuApi',)


class FoodMenuApi(APIView):

    class OutputSerializer(serializers.Serializer):

        class ItemSerializer(serializers.Serializer):
            name = serializers.CharField()
            calories_count = serializers.IntegerField()
            photo_url = serializers.URLField()

        items = ItemSerializer(many=True)
        at = serializers.DateField()

    def get(self, request: Request):
        try:
            food_menu_html = get_food_menu_html()
        except FoodMenuApiRequestError:
            raise APIException
        try:
            daily_food_menus = parse_food_menu_html(food_menu_html)
        except FoodMenuParseError:
            raise APIException

        serializer = self.OutputSerializer(daily_food_menus, many=True)
        response_data = {'food_menus': serializer.data}

        return Response(response_data)
