from rest_framework import status, serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from manas_id.exceptions import ManasIdDoesNotExistError
from manas_id.models import ManasId
from manas_id.selectors import get_manas_id_by_user_id
from manas_id.serializers import ManasIdSerializer

__all__ = ('ManasIdRetrieveApi', 'ManasIdListApi')


class ManasIdRetrieveApi(APIView):

    def get(self, request: Request, user_id: int):
        try:
            manas_id = get_manas_id_by_user_id(user_id)
        except ManasIdDoesNotExistError:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ManasIdSerializer(manas_id)
        return Response(serializer.data)


class ManasIdListApi(APIView):

    class LimitOffsetSerializer(serializers.Serializer):
        limit = serializers.IntegerField(min_value=1, max_value=100, default=10)
        offset = serializers.IntegerField(min_value=0, default=0)

    def get(self, request: Request):
        serializer = self.LimitOffsetSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data

        limit: int = serialized_data['limit']
        offset: int = serialized_data['offset']

        manas_ids = ManasId.objects.order_by('-born_at')
        manas_ids = manas_ids[offset:offset + limit + 1]

        is_end_of_list_reached = len(manas_ids) <= limit

        serializer = ManasIdSerializer(manas_ids, many=True)
        response_data = {
            'ok': True,
            'result': {
                'is_end_of_list_reached': is_end_of_list_reached,
                'manas_ids': serializer.data,
            },
        }
        return Response(response_data)
