from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from secret_messages.selectors import get_visible_themes

__all__ = ('ThemeListApi',)


class ThemeListApi(APIView):

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        description_template_text = serializers.CharField()
        button_text = serializers.CharField()

    def get(self, request: Request):
        secret_message_themes = get_visible_themes()
        serializer = self.OutputSerializer(secret_message_themes, many=True)
        return Response(serializer.data)
