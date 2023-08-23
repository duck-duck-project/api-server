from django.test import TestCase

from users.models import User, Contact
from users.services.contacts import (
    update_contact,
    create_contact
)


class ContactCreateServicesTests(TestCase):
    """Tests for the contact create services."""

    def setUp(self) -> None:
        """Set up the test case."""
        self.eldos = User.objects.create(
            id=123456789,
            username='usbtypec',
            fullname='Eldos',
        )
        self.alex = User.objects.create(
            id=987654321,
            username=None,
            fullname='Alexander',
        )

    def test_create_contact(self) -> None:
        contact, is_created = create_contact(
            of_user=self.eldos,
            to_user=self.alex,
            private_name='Alex',
            public_name='Alexender Pushkin',
        )
        self.assertEqual(contact.of_user, self.eldos)
        self.assertEqual(contact.to_user, self.alex)
        self.assertEqual(contact.private_name, 'Alex')
        self.assertEqual(contact.public_name, 'Alexender Pushkin')
        self.assertTrue(is_created)


class ContactUpdateServicesTests(TestCase):

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
        self.contact = Contact.objects.create(
            of_user=self.eldos,
            to_user=self.alexander,
            private_name='Alex',
            public_name='Alexender Pushkin',
        )

    def test_update_contact(self) -> None:
        is_updated = update_contact(
            contact_id=self.contact.id,
            private_name='Joseph',
            public_name='York',
            is_hidden=True,
        )
        self.assertTrue(is_updated)

        self.contact.refresh_from_db()

        self.assertEqual(self.contact.private_name, 'Joseph')
        self.assertEqual(self.contact.public_name, 'York')
        self.assertTrue(self.contact.is_hidden)

    def test_update_contact_not_found(self) -> None:
        is_updated = update_contact(
            contact_id=22,
            private_name='Joseph',
            public_name='York',
            is_hidden=True,
        )
        self.assertFalse(is_updated)
