import factory
from factory.django import DjangoModelFactory

__all__ = ('UserFactory',)


class UserFactory(DjangoModelFactory):
    class Meta:
        model = 'users.User'

    id = factory.Sequence(lambda n: n + 1000000)
    username = factory.Sequence(lambda n: f'username-{n}')
    fullname = factory.Sequence(lambda n: f'fullname-{n}')
    born_at = factory.Faker('date')
