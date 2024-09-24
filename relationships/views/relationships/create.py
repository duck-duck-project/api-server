from rest_framework import serializers, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from relationships.services import create_relationship
from users.serializers import UserPartialSerializer
from users.services.users import get_or_create_user

__all__ = ('RelationshipCreateApi',)


class RelationshipCreateApi(APIView):
    class InputSerializer(serializers.Serializer):
        first_user_id = serializers.IntegerField()
        second_user_id = serializers.IntegerField()

        def validate(self, data: dict) -> dict:
            if data['first_user_id'] == data['second_user_id']:
                raise serializers.ValidationError('Users must be different')
            return data

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        first_user = UserPartialSerializer()
        second_user = UserPartialSerializer()
        created_at = serializers.DateTimeField()

    def post(self, request: Request) -> Response:
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data: dict = serializer.validated_data

        first_user_id: int = serialized_data['first_user_id']
        second_user_id: int = serialized_data['second_user_id']

        first_user, _ = get_or_create_user(first_user_id)
        second_user, _ = get_or_create_user(second_user_id)

        relationship = create_relationship(
            first_user=first_user,
            second_user=second_user,
        )

        serializer = self.OutputSerializer(relationship)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
