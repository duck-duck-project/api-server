from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from secret_messages.exceptions import ThemeDoesNotExistError
from secret_messages.selectors import get_visible_themes, get_theme_by_id

__all__ = ('ThemeListApi', 'ThemeRetrieveApi')


class ThemeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    description_template_text = serializers.CharField()
    button_text = serializers.CharField()
    is_hidden = serializers.BooleanField()


class ThemeRetrieveApi(APIView):

    def get(self, request: Request, theme_id: int):
        try:
            theme = get_theme_by_id(theme_id)
        except ThemeDoesNotExistError:
            raise NotFound('Theme does not exist')
        serializer = ThemeSerializer(theme)
        return Response(serializer.data)


class ThemeListApi(APIView):

    class InputSerializer(serializers.Serializer):
        limit = serializers.IntegerField(default=50)
        offset = serializers.IntegerField(default=0)

    def get(self, request: Request):
        serializer = self.InputSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        limit: int = serialized_data['limit']
        offset: int = serialized_data['offset']

        themes = get_visible_themes(
            limit=limit + 1,
            offset=offset,
        )

        is_end_of_list_reached = len(themes) <= limit
        serializer = ThemeSerializer(themes[:limit], many=True)
        response_data = {
            'themes': serializer.data,
            'is_end_of_list_reached': is_end_of_list_reached,
        }
        return Response(response_data)
