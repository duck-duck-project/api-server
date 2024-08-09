from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

__all__ = ('RelationshipRetrieveApi',)

from relationships.selectors.relationships import get_active_relationship
from relationships.serializers import UserInRelationshipSerializer
from users.selectors.users import get_user_by_id


class RelationshipRetrieveApi(APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        first_user = UserInRelationshipSerializer()
        second_user = UserInRelationshipSerializer()
        created_at = serializers.DateTimeField()

    def get(self, request: Request, user_id: int) -> Response:

        user = get_user_by_id(user_id)
        get_active_relationship(user_id)

        response_data = {'ok': True}
        return Response(response_data)
