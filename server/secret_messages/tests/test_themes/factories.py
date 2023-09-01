import factory
from factory.django import DjangoModelFactory

from secret_messages.models.secret_message_themes import SecretMessageTheme

__all__ = ('ThemeFactory',)


class ThemeFactory(DjangoModelFactory):

    class Meta:
        model = SecretMessageTheme

    description_template_text = factory.LazyFunction(
        lambda: 'Message for {name}'
    )
    button_text = factory.Faker('word')
