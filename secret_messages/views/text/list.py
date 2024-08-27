from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from secret_messages.selectors.text import get_contacts_secret_messages
from users.selectors.contacts import (
    get_contact_ids_from_user_contacts,
    get_reversed_user_contact_or_none,
    get_user_contact_by_id,
)

__all__ = ('SecretTextMessageListApi',)


class SecretTextMessageListApi(APIView):

    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        text = serializers.CharField()
        sender_id = serializers.IntegerField()
        recipient_id = serializers.IntegerField()
        seen_at = serializers.DateTimeField(allow_null=True)
        created_at = serializers.DateTimeField()

    def get(self, request: Request, contact_id: int) -> Response:
        user_contact = get_user_contact_by_id(contact_id)
        reversed_user_contact = get_reversed_user_contact_or_none(user_contact)

        contact_ids = get_contact_ids_from_user_contacts((
            user_contact,
            reversed_user_contact
        ))

        secret_messages = get_contacts_secret_messages(contact_ids)

        serializer = self.OutputSerializer(secret_messages, many=True)
        response_data = {'secret_messages': serializer.data}
        return Response(response_data)
