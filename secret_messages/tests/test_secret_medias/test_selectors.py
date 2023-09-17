from django.test import TestCase

from secret_messages.models.secret_medias import SecretMedia
from secret_messages.selectors import get_secret_media_by_id
from users.models import Contact, User


class SecretMediaSelectorsTests(TestCase):

    def setUp(self) -> None:
        self.eldos = User.objects.create(
            id=23456789,
            fullname='Eldos',
            username='usbtypec',
        )
        self.alex = User.objects.create(id=12345678, fullname='Alex')
        self.contact = Contact.objects.create(
            of_user=self.eldos,
            to_user=self.alex,
            private_name='Alex',
            public_name='Alex',
        )
        self.secret_media = SecretMedia.objects.create(
            name='Beautiful photo',
            contact=self.contact,
            file_id='adq3jh4k5l6',
            media_type=SecretMedia.MediaType.PHOTO,
        )

    def test_get_secret_media_by_id(self) -> None:
        secret_media = get_secret_media_by_id(self.secret_media.id)
        self.assertEqual(secret_media, self.secret_media)
