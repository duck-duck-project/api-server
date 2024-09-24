from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from relationships.selectors import get_active_relationship
from relationships.services import break_up

__all__ = ('RelationshipBreakUpApi',)


class RelationshipBreakUpApi(APIView):

    def delete(self, request: Request, user_id: int) -> Response:
        relationship = get_active_relationship(user_id)
        break_up(relationship.id)

        return Response(status=status.HTTP_200_OK)
