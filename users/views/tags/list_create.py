from rest_framework import serializers, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import Tag
from users.services.users import get_or_create_user

__all__ = ('TagListCreateApi',)


class TagListCreateApi(APIView):

    class OutputListSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        text = serializers.CharField()
        weight = serializers.ChoiceField(choices=Tag.Weight.choices)
        created_at = serializers.DateTimeField()
        of_user_fullname = serializers.CharField(source='of_user__fullname')
        of_user_username = serializers.CharField(
            allow_null=True,
            source='of_user__username',
        )

    class InputCreateSerializer(serializers.Serializer):
        to_user_id = serializers.IntegerField()
        of_user_id = serializers.IntegerField()
        text = serializers.CharField(max_length=32)
        weight = serializers.ChoiceField(choices=Tag.Weight.choices)

    class OutputCreateSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        text = serializers.CharField(max_length=32)
        weight = serializers.ChoiceField(choices=Tag.Weight.choices)
        created_at = serializers.DateTimeField()
        of_user_fullname = serializers.CharField(source='of_user.fullname')
        of_user_username = serializers.CharField(
            allow_null=True,
            source='of_user.username',
        )

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
        serializer = self.OutputListSerializer(tags, many=True)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        serializer = self.InputCreateSerializer(data=request.data)
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

        serializer = self.OutputCreateSerializer(tag)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
