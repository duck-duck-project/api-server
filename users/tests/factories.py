import factory
from factory.django import DjangoModelFactory

from users.models.users import User

__all__ = ('UserFactory',)


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    id = factory.Sequence(lambda n: n)
