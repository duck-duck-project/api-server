from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from users.selectors.birthdays import get_user_contact_birthdays

__all__ = ('UserContactBirthdayListApi',)


class UserContactBirthdayListApi(APIView):
    class OutputSerializer(serializers.Serializer):
        user_id = serializers.IntegerField()
        fullname = serializers.CharField()
        username = serializers.CharField(allow_null=True)
        born_on = serializers.DateField()

    def get(self, request: Request, user_id: int) -> Response:
        contact_birthdays = get_user_contact_birthdays(user_id)
        serializer = self.OutputSerializer(contact_birthdays, many=True)
        return Response({'result': serializer.data, 'ok': True})
