from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from django.db.models import QuerySet

from users.exceptions import ContactNotFoundError
from users.models import Contact, Theme, User

__all__ = (
    'get_user_contact_by_id',
    'get_not_deleted_contacts_by_user_id',
    'get_user_contacts',
    'get_reversed_user_contact_or_none',
    'UserWithThemeDTO',
    'UserContactDTO',
    'ThemeDTO',
    'get_contact_ids_from_user_contacts',
)

CONTACTS_SORTING_STRATEGY_TO_FIELD_NAME = {
    User.ContactsSortingStrategy.CREATION_TIME.value: 'created_at',
    User.ContactsSortingStrategy.PUBLIC_NAME.value: 'public_name',
    User.ContactsSortingStrategy.PRIVATE_NAME.value: 'private_name',
}


@dataclass(frozen=True, slots=True)
class ThemeDTO:
    id: UUID
    is_hidden: bool
    secret_message_template_text: str
    secret_media_template_text: str
    secret_message_view_button_text: str
    secret_message_delete_button_text: str
    secret_message_read_confirmation_text: str
    secret_message_deleted_confirmation_text: str
    secret_message_deleted_text: str
    secret_message_missing_text: str
    created_at: datetime


@dataclass(frozen=True, slots=True)
class UserDTO:
    id: int
    fullname: str
    username: str | None


@dataclass(frozen=True, slots=True)
class UserWithCanReceiveNotificationsAndProfilePhotoDTO(UserDTO):
    can_receive_notifications: bool
    profile_photo_url: str | None


@dataclass(frozen=True, slots=True)
class UserWithThemeDTO(UserDTO):
    theme: ThemeDTO


@dataclass(frozen=True, slots=True)
class ContactDTO:
    id: int
    user: UserWithCanReceiveNotificationsAndProfilePhotoDTO
    public_name: str
    private_name: str
    is_hidden: bool
    theme: ThemeDTO
    created_at: datetime


@dataclass(frozen=True, slots=True)
class ContactsSortingDTO:
    strategy: int
    is_reversed: bool


@dataclass(frozen=True, slots=True)
class UserContactsDTO:
    user: UserWithThemeDTO
    contacts: list[ContactDTO]
    sorting: ContactsSortingDTO


@dataclass(frozen=True, slots=True)
class UserContactDTO:
    user: UserWithThemeDTO
    contact: ContactDTO


def get_contact_ids_from_user_contacts(
        user_contacts: Iterable[UserContactDTO | None],
) -> set[int]:
    return {
        user_contact.contact.id
        for user_contact in user_contacts
        if user_contact is not None
    }


def map_contacts_sorting_to_dto(user: User) -> ContactsSortingDTO:
    return ContactsSortingDTO(
        strategy=user.contacts_sorting_strategy,
        is_reversed=user.is_contacts_sorting_reversed,
    )


def map_theme_to_dto(theme: Theme | None) -> ThemeDTO | None:
    if theme is None:
        return
    return ThemeDTO(
        id=theme.id,
        is_hidden=theme.is_hidden,
        secret_message_template_text=theme.secret_message_template_text,
        secret_media_template_text=theme.secret_media_template_text,
        secret_message_view_button_text=theme.secret_message_view_button_text,
        secret_message_delete_button_text=(
            theme.secret_message_delete_button_text
        ),
        secret_message_read_confirmation_text=(
            theme.secret_message_read_confirmation_text
        ),
        secret_message_deleted_confirmation_text=(
            theme.secret_message_deleted_confirmation_text
        ),
        secret_message_deleted_text=theme.secret_message_deleted_text,
        secret_message_missing_text=theme.secret_message_missing_text,
        created_at=theme.created_at,
    )


def map_user_with_profile_photo_url_and_can_receive_notifications_to_dto(
        user: User,
) -> UserWithCanReceiveNotificationsAndProfilePhotoDTO:
    return UserWithCanReceiveNotificationsAndProfilePhotoDTO(
        id=user.id,
        fullname=user.fullname,
        username=user.username,
        profile_photo_url=user.profile_photo_url,
        can_receive_notifications=user.can_receive_notifications,
    )


def map_user_with_theme_to_dto(user: User) -> UserWithThemeDTO:
    return UserWithThemeDTO(
        id=user.id,
        fullname=user.fullname,
        username=user.username,
        theme=map_theme_to_dto(user.theme),
    )


def map_contact_to_dto(contact: Contact) -> ContactDTO:
    return ContactDTO(
        id=contact.id,
        user=map_user_with_profile_photo_url_and_can_receive_notifications_to_dto(contact.to_user),
        public_name=contact.public_name,
        private_name=contact.private_name,
        is_hidden=contact.is_hidden,
        theme=map_theme_to_dto(contact.to_user.theme),
        created_at=contact.created_at,
    )


def get_user_contacts(user: User) -> UserContactsDTO:
    contacts = (
        Contact.objects
        .select_related('to_user', 'to_user__theme')
        .filter(
            of_user_id=user.id,
            is_deleted=False,
        )
    )
    contacts_dtos: list[ContactDTO] = [
        map_contact_to_dto(contact)
        for contact in contacts
    ]
    return UserContactsDTO(
        user=map_user_with_theme_to_dto(user),
        contacts=contacts_dtos,
        sorting=map_contacts_sorting_to_dto(user),
    )


def get_user_contact_by_id(contact_id: int) -> UserContactDTO:
    """Retrieve contact instance by ID.

    Args:
        contact_id: ID of contact.

    Returns:
        Contact instance if exists.

    Raises:
        ContactNotFoundError: If contact does not exist.
    """
    try:
        contact = (
            Contact.objects
            .select_related(
                'of_user',
                'to_user',
                'of_user__theme',
                'to_user__theme',
            )
            .get(id=contact_id, is_deleted=False)
        )
    except Contact.DoesNotExist:
        raise ContactNotFoundError

    return UserContactDTO(
        user=map_user_with_theme_to_dto(contact.of_user),
        contact=map_contact_to_dto(contact),
    )


def get_not_deleted_contacts_by_user_id(user: User) -> QuerySet[Contact]:
    """Retrieve contacts of user that are not marked as deleted.

    Args:
        user: User object.

    Returns:
        QuerySet of contacts.
    """

    contacts = (
        Contact.objects
        .select_related(
            'of_user',
            'to_user',
            'of_user__theme',
            'to_user__theme',
        )
        .filter(of_user=user, is_deleted=False)
    )

    sorting_field_name = CONTACTS_SORTING_STRATEGY_TO_FIELD_NAME[
        user.contacts_sorting_strategy
    ]
    if user.is_contacts_sorting_reversed:
        sorting_field_name = f'-{sorting_field_name}'

    return contacts.order_by(sorting_field_name)


def get_reversed_user_contact_or_none(
        user_contact: UserContactDTO
) -> UserContactDTO | None:
    try:
        contact = (
            Contact.objects
            .select_related(
                'of_user',
                'to_user',
                'of_user__theme',
                'to_user__theme',
            )
            .get(
                of_user_id=user_contact.contact.user.id,
                to_user_id=user_contact.user.id,
                is_deleted=False,
            )
        )
    except Contact.DoesNotExist:
        return

    return UserContactDTO(
        user=map_user_with_theme_to_dto(contact.of_user),
        contact=map_contact_to_dto(contact),
    )
