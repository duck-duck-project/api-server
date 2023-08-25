from uuid import uuid4

from django.urls import reverse
from rest_framework.test import APITestCase

from secret_messages.models.secret_medias import SecretMedia
from users.models import Contact, User


class SecretMediaCreateApiTests(APITestCase):

    def setUp(self) -> None:
        self.eldos = User.objects.create(
            id=123456789,
            username='usbtypec',
            fullname='Eldos',
        )
        self.alex = User.objects.create(id=234561234, fullname='Alex')
        self.contact = Contact.objects.create(
            of_user=self.eldos,
            to_user=self.alex,
            private_name='Alex',
            public_name='Alex',
        )

    def test_create_secret_media(self) -> None:
        url = reverse('secret-medias-create')
        request_data = {
            'file_id': 'ask13jiaosjio23j4',
            'name': 'Beautiful photo',
            'contact_id': self.contact.id,
            'media_type': SecretMedia.MediaType.PHOTO.value,
        }
        response = self.client.post(url, request_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['file_id'], request_data['file_id'])
        self.assertEqual(response.data['name'], request_data['name'])
        self.assertEqual(
            response.data['contact']['id'],
            request_data['contact_id'],
        )
        self.assertEqual(
            response.data['media_type'],
            request_data['media_type'],
        )


class SecretMediaRetrieveApiTests(APITestCase):

    def setUp(self) -> None:
        self.eldos = User.objects.create(
            id=123456789,
            username='usbtypec',
            fullname='Eldos',
        )
        self.alex = User.objects.create(id=234561234, fullname='Alex')
        self.contact = Contact.objects.create(
            of_user=self.eldos,
            to_user=self.alex,
            private_name='Alex',
            public_name='Alex',
        )
        self.secret_media = SecretMedia.objects.create(
            file_id='ask13jiaosjio23j4',
            name='Beautiful photo',
            contact=self.contact,
            media_type=SecretMedia.MediaType.PHOTO.value,
        )

    def test_retrieve_secret_media(self) -> None:
        url = reverse('secret-medias-retrieve', args=(self.secret_media.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['file_id'], self.secret_media.file_id)
        self.assertEqual(response.data['name'], self.secret_media.name)
        self.assertEqual(
            response.data['contact']['id'],
            self.secret_media.contact.id,
        )
        self.assertEqual(
            response.data['media_type'],
            self.secret_media.media_type,
        )

    def test_retrieve_secret_media_does_not_exist(self) -> None:
        url = reverse('secret-medias-retrieve', args=(uuid4(),))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['detail'], 'Secret media does not exist')
