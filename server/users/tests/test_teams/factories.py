import factory
from factory.django import DjangoModelFactory

__all__ = ('TeamFactory',)


class TeamFactory(DjangoModelFactory):
    class Meta:
        model = 'users.Team'

    name = factory.Sequence(lambda n: f'team-{n}')
