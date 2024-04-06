from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from wishes.exceptions import NoWishesError
from wishes.selectors import get_random_wish

__all__ = ('RandomWishApi',)


class RandomWishApi(APIView):
    class OutputSerializer(serializers.Serializer):
        text = serializers.CharField()

    def get(self, request: Request) -> Response:
        try:
            wish = get_random_wish()
        except NoWishesError:
            raise NotFound('No wishes')

        serializer = self.OutputSerializer(wish)
        return Response(serializer.data)
