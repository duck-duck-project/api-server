from django.test import TestCase

from users.exceptions import ContactDoesNotExistError
from users.selectors.contacts import (
    get_not_deleted_contact_by_id,
    get_not_deleted_contacts_by_user_id,
)
from users.tests.test_contacts.factories import ContactFactory
from users.tests.test_users.factories import UserFactory


class ContactSelectorsTests(TestCase):

    def setUp(self) -> None:
        self.user = UserFactory()
        self.contact_1 = ContactFactory()
        self.contact_2 = ContactFactory(is_deleted=True)

    def test_get_contact_by_user(self) -> None:
        contact = get_not_deleted_contact_by_id(self.contact_1.id)
        self.assertEqual(contact, self.contact_1)

    def test_get_contact_by_user_does_not_exists(self) -> None:
        with self.assertRaises(ContactDoesNotExistError):
            get_not_deleted_contact_by_id(self.user.id)

    def test_get_contacts_by_user_id(self) -> None:
        contacts = get_not_deleted_contacts_by_user_id(
            user_id=self.contact_1.of_user.id
        )
        self.assertEqual(contacts.count(), 1)
        self.assertEqual(contacts.first(), self.contact_1)
