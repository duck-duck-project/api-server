import factory
from factory.django import DjangoModelFactory

from users.tests.test_users.factories import UserFactory

__all__ = ('ContactFactory',)


class ContactFactory(DjangoModelFactory):
    class Meta:
        model = 'users.Contact'

    of_user = factory.SubFactory(UserFactory)
    to_user = factory.SubFactory(UserFactory)
    private_name = factory.Sequence(lambda n: f'private_name_{n}')
    public_name = factory.Sequence(lambda n: f'public_name_{n}')
