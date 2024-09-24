from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from relationships.selectors import (
    get_active_relationship,
    get_relationship_by_id,
)
from relationships.services import break_up
from users.serializers import UserPartialSerializer

__all__ = ('RelationshipBreakUpApi',)


class RelationshipBreakUpApi(APIView):

    class OutputSerializer(serializers.Serializer):
        first_user = UserPartialSerializer()
        second_user = UserPartialSerializer()
        created_at = serializers.DateTimeField()
        broke_up_at = serializers.DateTimeField()
        level = serializers.IntegerField()

    def delete(self, request: Request, user_id: int) -> Response:
        relationship = get_active_relationship(user_id)
        break_up(relationship.id)
        relationship = get_relationship_by_id(relationship.id)
        serializer = self.OutputSerializer(relationship)
        return Response(serializer.data)
