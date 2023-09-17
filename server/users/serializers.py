from rest_framework import serializers

__all__ = ('UserPartialSerializer',)


class UserPartialSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    fullname = serializers.CharField()
