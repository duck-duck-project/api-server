from django.test import TestCase

from users.tests.test_contacts.factories import ContactFactory


class ContactModelTestCase(TestCase):

    def setUp(self) -> None:
        self.contact = ContactFactory(public_name='John Doe')

    def test_contact_str(self):
        self.assertEqual(str(self.contact), 'John Doe')
