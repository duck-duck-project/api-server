from rest_framework import serializers, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import Tag
from users.selectors.tags import get_tag_by_id
from users.serializers import UserPartialSerializer
from users.services.tags import create_tag, delete_tag
from users.services.users import get_or_create_user

__all__ = ('TagCreateDeleteApi',)


class TagCreateDeleteApi(APIView):

    class InputDeleteSerializer(serializers.Serializer):
        user_id = serializers.IntegerField()
        tag_id = serializers.IntegerField()

    class InputCreateSerializer(serializers.Serializer):
        to_user_id = serializers.IntegerField()
        of_user_id = serializers.IntegerField()
        text = serializers.CharField(max_length=32)
        weight = serializers.ChoiceField(choices=Tag.Weight.choices)

    class OutputCreateSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        of_user = UserPartialSerializer()
        to_user = UserPartialSerializer()
        text = serializers.CharField(max_length=32)
        weight = serializers.ChoiceField(choices=Tag.Weight.choices)
        created_at = serializers.DateTimeField()

    def post(self, request: Request) -> Response:
        serializer = self.InputCreateSerializer(data=request.data)
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

        serializer = self.OutputCreateSerializer(tag)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request: Request) -> Response:
        serializer = self.InputDeleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        user_id: int = serialized_data['user_id']
        tag_id: int = serialized_data['tag_id']

        tag = get_tag_by_id(tag_id)

        delete_tag(tag=tag, user_id=user_id)

        return Response(status=status.HTTP_204_NO_CONTENT)
