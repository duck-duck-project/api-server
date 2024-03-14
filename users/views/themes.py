from uuid import UUID

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from users.selectors.themes import get_theme_by_id, get_visible_themes
from users.serializers import ThemeSerializer

__all__ = ('ThemeListApi', 'ThemeRetrieveApi')


class ThemeListApi(APIView):
    OutputSerializer = ThemeSerializer

    def get(self, request: Request):
        themes = get_visible_themes()
        serializer = self.OutputSerializer(themes, many=True)
        return Response({'ok': True, 'result': serializer.data})


class ThemeRetrieveApi(APIView):
    OutputSerializer = ThemeSerializer

    def get(self, request: Request, theme_id: UUID):
        theme = get_theme_by_id(theme_id)
        serializer = self.OutputSerializer(theme)
        return Response({'ok': True, 'result': serializer.data})
