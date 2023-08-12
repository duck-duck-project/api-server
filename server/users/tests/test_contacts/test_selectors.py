from django.test import TestCase

from users.exceptions import ContactDoesNotExistError
from users.models import Contact, User
from users.selectors.contacts import get_contact_by_id, get_contacts_by_user_id


class ContactSelectorsTests(TestCase):

    def setUp(self) -> None:
        self.eldos = User.objects.create(
            id=87654321,
            username='usbtypec',
            fullname='Eldos',
        )
        self.alexander = User.objects.create(
            id=12345678,
            username=None,
            fullname='Alexander',
        )
        self.shahadat = User.objects.create(
            id=52572345,
            username=None,
            fullname='Shahadat',
        )
        self.contact1 = Contact.objects.create(
            of_user=self.eldos,
            to_user=self.alexander,
            private_name='Alex',
            public_name='Alexender Pushkin',
        )
        self.contact2 = Contact.objects.create(
            of_user=self.eldos,
            to_user=self.shahadat,
            private_name='Shahadat 🌙',
            public_name='Yng Moon',
        )

    def test_get_contact_by_user(self) -> None:
        contact = get_contact_by_id(self.contact1.id)
        self.assertEqual(contact, self.contact1)

    def test_get_contact_by_user_does_not_exists(self) -> None:
        with self.assertRaises(ContactDoesNotExistError) as error:
            get_contact_by_id(22)
        self.assertEqual(error.exception.contact_id, 22)

    def test_get_contacts_by_user_id(self) -> None:
        contacts = get_contacts_by_user_id(self.eldos.id)
        self.assertEqual(contacts.count(), 2)

        for contact in contacts:
            self.assertEqual(contact.of_user, self.eldos)
