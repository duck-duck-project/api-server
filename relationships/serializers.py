from rest_framework import serializers

__all__ = ('UserInRelationshipSerializer',)


class UserInRelationshipSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    fullname = serializers.CharField()
    username = serializers.CharField(allow_null=True)
