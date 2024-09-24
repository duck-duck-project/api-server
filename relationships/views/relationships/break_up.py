from rest_framework import serializers, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from relationships.selectors import get_active_relationship
from relationships.services import break_up

__all__ = ('RelationshipBreakUpApi',)


class RelationshipBreakUpApi(APIView):

    class InputSerializer(serializers.Serializer):
        user_id = serializers.IntegerField()

    def post(self, request: Request) -> Response:
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data: dict = serializer.data

        user_id: int = serialized_data['user_id']

        relationship = get_active_relationship(user_id)
        break_up(relationship.id)

        return Response(status=status.HTTP_200_OK)
