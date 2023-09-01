import factory

import models

__all__ = ('User',)


class User(factory.Factory):

    class Meta:
        model = models.User

    id = factory.Sequence(lambda n: n + 100_000)
    fullname = factory.Faker('name')
    username = factory.Faker('user_name')
    is_premium = factory.Faker('pybool')
    can_be_added_to_contacts = factory.Faker('pybool')
    secret_message_theme = None
    profile_photo_url = None
    is_banned = factory.Faker('pybool')
    can_receive_notifications = factory.Faker('pybool')
    born_at = factory.Faker('date')
