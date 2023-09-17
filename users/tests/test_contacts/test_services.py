from django.test import TestCase

from users.services.contacts import update_contact, create_contact
from users.tests.test_contacts.factories import ContactFactory
from users.tests.test_users.factories import UserFactory


class ContactCreateServicesTests(TestCase):
    """Tests for the contact create services."""

    def setUp(self) -> None:
        """Set up the test case."""
        self.user_1 = UserFactory()
        self.user_2 = UserFactory()

    def test_create_contact(self) -> None:
        contact, is_created = create_contact(
            of_user=self.user_1,
            to_user=self.user_2,
            private_name='Alex',
            public_name='Alexender Pushkin',
        )
        self.assertEqual(contact.of_user, self.user_1)
        self.assertEqual(contact.to_user, self.user_2)
        self.assertEqual(contact.private_name, 'Alex')
        self.assertEqual(contact.public_name, 'Alexender Pushkin')
        self.assertTrue(is_created)


class ContactUpdateServicesTests(TestCase):

    def setUp(self) -> None:
        self.contact = ContactFactory()

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
