from django.test import TestCase

from secret_messages.exceptions import SecretMediaAlreadyExistsError
from secret_messages.models.secret_medias import SecretMedia
from secret_messages.services import create_secret_media
from users.models import User, Contact


class SecretMediaServicesTests(TestCase):

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

    def test_create_secret_media(self) -> None:
        secret_media = create_secret_media(
            name='Beautiful photo',
            contact=self.contact,
            file_id='adq3jh4k5l6',
            media_type=SecretMedia.MediaType.PHOTO,
        )
        self.assertEqual(
            secret_media,
            SecretMedia.objects.get(id=secret_media.id),
        )

    def test_create_secret_media_already_exists_error(self) -> None:
        secret_media = create_secret_media(
            name='Beautiful photo',
            contact=self.contact,
            file_id='adq3jh4k5l6',
            media_type=SecretMedia.MediaType.PHOTO,
        )
        with self.assertRaises(SecretMediaAlreadyExistsError):
            create_secret_media(
                name='Beautiful photo',
                contact=self.contact,
                file_id='adq3jh4k5l6',
                media_type=SecretMedia.MediaType.PHOTO,
            )
