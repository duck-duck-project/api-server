from rest_framework import serializers, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import Tag
from users.serializers import UserPartialSerializer
from users.services.tags import create_tag
from users.services.users import get_or_create_user

__all__ = ('TagCreateApi',)


class TagCreateApi(APIView):

    class InputSerializer(serializers.Serializer):
        to_user_id = serializers.IntegerField()
        of_user_id = serializers.IntegerField()
        text = serializers.CharField(max_length=32)
        weight = serializers.ChoiceField(choices=Tag.Weight.choices)

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        of_user = UserPartialSerializer()
        to_user = UserPartialSerializer()
        text = serializers.CharField(max_length=32)
        weight = serializers.ChoiceField(choices=Tag.Weight.choices)
        created_at = serializers.DateTimeField()

    def post(self, request: Request) -> Response:
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        of_user_id: int = serialized_data['of_user_id']
        to_user_id: int = serialized_data['to_user_id']
        text: str = serialized_data['text']
        weight: Tag.Weight = Tag.Weight(serialized_data['weight'])

        of_user, _ = get_or_create_user(of_user_id)
        to_user, _ = get_or_create_user(to_user_id)

        tag = create_tag(
            of_user=of_user,
            to_user=to_user,
            text=text,
            weight=weight
        )

        serializer = self.OutputSerializer(tag)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
