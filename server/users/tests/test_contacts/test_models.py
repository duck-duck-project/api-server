from django.test import TestCase

from users.models import Contact


class ContactModelTestCase(TestCase):

    def test_contact_str(self):
        contact = Contact(public_name='John Doe')
        self.assertEqual(str(contact), 'John Doe')
