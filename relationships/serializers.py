from rest_framework import serializers

from users.serializers import UserPartialSerializer


class RelationshipOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_user = UserPartialSerializer()
    second_user = UserPartialSerializer()
    created_at = serializers.DateTimeField()
