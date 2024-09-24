from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from relationships.selectors import get_active_relationship
from users.serializers import UserPartialSerializer

__all__ = ('RelationshipRetrieveApi',)


class RelationshipRetrieveApi(APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        first_user = UserPartialSerializer()
        second_user = UserPartialSerializer()
        created_at = serializers.DateTimeField()
        level = serializers.IntegerField()
        experience = serializers.IntegerField()
        next_level_experience_threshold = serializers.IntegerField()

    def get(self, request: Request, user_id: int) -> Response:
        relationship = get_active_relationship(user_id)
        serializer = self.OutputSerializer(relationship)
        return Response(serializer.data)
