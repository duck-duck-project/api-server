from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import Tag
from users.selectors.tags import get_tags_by_user_id
from users.serializers import UserPartialSerializer

__all__ = ('TagListApi',)


class TagSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    of_user = UserPartialSerializer()
    text = serializers.CharField()
    weight = serializers.ChoiceField(choices=Tag.Weight.choices)
    created_at = serializers.DateTimeField()


class TagListApi(APIView):

    class OutputSerializer(serializers.Serializer):
        user = UserPartialSerializer()
        tags = TagSerializer(many=True)

    def get(self, request: Request, user_id: int) -> Response:
        tags = get_tags_by_user_id(user_id)
        serializer = self.OutputSerializer(tags)
        return Response(serializer.data)
