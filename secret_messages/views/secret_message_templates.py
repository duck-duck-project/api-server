from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from secret_messages.selectors import (
    get_secret_message_description_templates,
    get_secret_message_button_templates,
)

__all__ = (
    'SecretMessageButtonTemplateListApi',
    'SecretMessageDescriptionTemplateListApi',
)


class SecretMessageDescriptionTemplateListApi(APIView):

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        text = serializers.CharField()
        created_at = serializers.DateTimeField()

    def get(self, request: Request):
        templates = get_secret_message_description_templates()
        serializer = self.OutputSerializer(templates, many=True)
        return Response(serializer.data)


class SecretMessageButtonTemplateListApi(APIView):

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        text = serializers.CharField()
        created_at = serializers.DateTimeField()

    def get(self, request: Request):
        templates = get_secret_message_button_templates()
        serializer = self.OutputSerializer(templates, many=True)
        return Response(serializer.data)
