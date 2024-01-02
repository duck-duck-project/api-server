from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from manas_id.exceptions import ManasIdDoesNotExistError
from manas_id.selectors import get_manas_id_by_user_id
from manas_id.serializers import ManasIdSerializer

__all__ = ('ManasIdRetrieveApi',)


class ManasIdRetrieveApi(APIView):

    def get(self, request: Request, user_id: int):
        try:
            manas_id = get_manas_id_by_user_id(user_id)
        except ManasIdDoesNotExistError:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ManasIdSerializer(manas_id)
        return Response(serializer.data)
