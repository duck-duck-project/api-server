from services import can_create_new_contact


def test_can_create_new_contact_basic():
    assert can_create_new_contact(contacts_count=3, is_premium=False)


def test_can_create_new_contact_contacts_limit():
    assert not can_create_new_contact(contacts_count=5, is_premium=False)


def test_can_create_new_contact_is_premium():
    assert can_create_new_contact(contacts_count=10, is_premium=True)


def test_can_create_new_contact_is_premium_and_contacts_limit():
    assert can_create_new_contact(contacts_count=5, is_premium=True)


def test_can_create_new_contact_negative_contacts_count():
    assert can_create_new_contact(contacts_count=-3, is_premium=False)
