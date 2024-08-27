from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from users.selectors.contacts import get_user_contacts
from users.serializers import ContactSerializer, UserPartialWithThemeSerializer
from users.services.users import get_or_create_user

__all__ = ('UserContactListApi',)


class UserContactListApi(APIView):

    class OutputSerializer(serializers.Serializer):
        class SortingSerializer(serializers.Serializer):
            strategy = serializers.ChoiceField(
                choices=User.ContactsSortingStrategy.choices,
            )
            is_reversed = serializers.BooleanField()

        user = UserPartialWithThemeSerializer()
        contacts = ContactSerializer(many=True)
        sorting = SortingSerializer()

    def get(self, request: Request, user_id: int):
        user, _ = get_or_create_user(user_id)
        user_contacts = get_user_contacts(user)
        serializer = self.OutputSerializer(user_contacts)
        response_data = {'contacts': serializer.data}
        return Response(response_data)
