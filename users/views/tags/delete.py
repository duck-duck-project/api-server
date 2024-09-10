from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from users.services.tags import delete_tag_by_id

__all__ = ('TagDeleteApi',)


class TagDeleteApi(APIView):

    def delete(self, request: Request, tag_id: int) -> Response:
        is_deleted = delete_tag_by_id(tag_id)
        status_code = (
            status.HTTP_204_NO_CONTENT
            if is_deleted else status.HTTP_404_NOT_FOUND
        )
        return Response(status=status_code)
