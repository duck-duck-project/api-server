from rest_framework import serializers

from users.models import Theme, User

__all__ = ('UserPartialSerializer', 'ThemeSerializer', 'UserSerializer')


class UserPartialSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    fullname = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        depth = 1


class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = '__all__'
