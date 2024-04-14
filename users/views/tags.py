from rest_framework import serializers, status
from rest_framework.exceptions import APIException, NotFound
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import Tag
from users.services.users import get_or_create_user

__all__ = ('TagListApi', 'TagDeleteApi', 'TagCreateApi')


class TagListApi(APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        text = serializers.CharField()
        weight = serializers.ChoiceField(choices=Tag.Weight.choices)
        created_at = serializers.DateTimeField()
        of_user_fullname = serializers.CharField(source='of_user__fullname')
        of_user_username = serializers.CharField(allow_null=True,
                                                 source='of_user__username')

    def get(self, request: Request, user_id: int) -> Response:
        tags = (
            Tag.objects
            .select_related('of_user')
            .filter(to_user_id=user_id)
            .values(
                'id',
                'text',
                'weight',
                'created_at',
                'of_user__fullname',
                'of_user__username',
            )
            .order_by('weight', '-created_at')
        )
        serializer = self.OutputSerializer(tags, many=True)
        response_data = {'ok': True, 'result': serializer.data}
        return Response(response_data)


class TagCreateApi(APIView):
    class InputSerializer(serializers.Serializer):
        to_user_id = serializers.IntegerField()
        of_user_id = serializers.IntegerField()
        text = serializers.CharField(max_length=32)
        weight = serializers.ChoiceField(choices=Tag.Weight.choices)

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        text = serializers.CharField(max_length=32)
        weight = serializers.ChoiceField(choices=Tag.Weight.choices)
        created_at = serializers.DateTimeField()
        of_user_fullname = serializers.CharField(source='of_user.fullname')
        of_user_username = serializers.CharField(allow_null=True,
                                                 source='of_user.username')

    def post(self, request: Request) -> Response:
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        of_user_id: int = serialized_data['of_user_id']
        to_user_id: int = serialized_data['to_user_id']
        text: str = serialized_data['text']
        weight: Tag.Weight = serialized_data['weight']

        of_user, _ = get_or_create_user(of_user_id)
        to_user, _ = get_or_create_user(to_user_id)

        tag = Tag.objects.create(
            of_user=of_user,
            to_user=to_user,
            text=text,
            weight=weight,
        )

        serializer = self.OutputSerializer(tag)
        response_data = {'ok': True, 'result': serializer.data}
        return Response(response_data, status=status.HTTP_201_CREATED)


class TagDeleteApi(APIView):

    def delete(self, request: Request, user_id: int, tag_id: int) -> Response:
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            raise NotFound('Tag not found')
        if tag.to_user_id != user_id:
            error = APIException('Only owner can remove tag')
            error.status_code = status.HTTP_403_FORBIDDEN
            raise error
        tag.delete()
        return Response({'ok': True})
