from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.serializers import UserSerializer

__all__ = ('UserApi',)


class UserApi(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
