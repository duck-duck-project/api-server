import factory
from factory.django import DjangoModelFactory

from relationships.models import Relationship
from users.tests.factories import UserFactory

__all__ = ('RelationshipFactory',)


class RelationshipFactory(DjangoModelFactory):
    class Meta:
        model = Relationship

    first_user = factory.SubFactory(UserFactory)
    second_user = factory.SubFactory(UserFactory)
