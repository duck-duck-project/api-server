from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol
from uuid import UUID

from secret_messages.exceptions import SecretTextMessageNotFoundError
from secret_messages.models.secret_messages import SecretTextMessage
from users.selectors.contacts import ThemeDTO

__all__ = (
    'get_secret_text_message_by_id',
    'ContactSecretTextMessageDTO',
    'SecretTextMessageDTO',
    'map_user_to_partial_dto',
    'get_contacts_secret_messages',
    'UserPartialDTO',
)


@dataclass(frozen=True, slots=True)
class UserPartialDTO:
    id: int
    fullname: str
    username: str | None


@dataclass(frozen=True, slots=True)
class UserWithCanReceiveNotificationsDTO(UserPartialDTO):
    can_receive_notifications: bool


@dataclass(frozen=True, slots=True)
class SecretTextMessageDTO:
    id: UUID
    text: str
    sender: UserPartialDTO
    recipient: UserWithCanReceiveNotificationsDTO
    theme: ThemeDTO | None
    deleted_at: datetime | None
    seen_at: datetime | None
    created_at: datetime


@dataclass(frozen=True, slots=True)
class ContactSecretTextMessageDTO:
    id: UUID
    text: str
    sender_id: int
    recipient_id: int
    seen_at: datetime | None
    created_at: datetime


class HasIdAndFullnameAndUsername(Protocol):
    id: int
    fullname: str
    username: str | None


class HasIdAndFullnameAndUsernameAndCanReceiveNotifications(
    HasIdAndFullnameAndUsername
):
    can_receive_notifications: bool


def map_user_to_partial_dto(
        user: HasIdAndFullnameAndUsername,
) -> UserPartialDTO:
    return UserPartialDTO(
        id=user.id,
        fullname=user.fullname,
        username=user.username,
    )


def map_user_to_with_can_receive_notifications_dto(
        user: HasIdAndFullnameAndUsernameAndCanReceiveNotifications,
) -> UserWithCanReceiveNotificationsDTO:
    return UserWithCanReceiveNotificationsDTO(
        id=user.id,
        fullname=user.fullname,
        username=user.username,
        can_receive_notifications=user.can_receive_notifications,
    )


def get_secret_text_message_by_id(
        secret_text_message_id: UUID,
) -> SecretTextMessageDTO:
    """Get secret message by ID.

    Args:
        secret_text_message_id: ID of the secret message.

    Returns:
        SecretTextMessageDTO object.

    Raises:
        SecretTextMessageNotFoundError: If secret message with the given ID
    """
    try:
        secret_text_message = (
            SecretTextMessage.objects
            .select_related(
                'contact',
                'contact__of_user',
                'contact__of_user__theme',
                'contact__theme',
            )
            .only(
                'id',
                'text',
                'contact__of_user__id',
                'contact__of_user__fullname',
                'contact__of_user__username',
                'contact__theme',
                'contact__of_user__theme',
                'seen_at',
                'created_at',
            )
            .get(id=secret_text_message_id, deleted_at__isnull=True)
        )
    except SecretTextMessage.DoesNotExist:
        raise SecretTextMessageNotFoundError

    contact = secret_text_message.contact

    theme = contact.theme or contact.of_user.theme

    return SecretTextMessageDTO(
        id=secret_text_message.id,
        text=secret_text_message.text,
        sender=map_user_to_partial_dto(contact.of_user),
        recipient=map_user_to_with_can_receive_notifications_dto(
            user=contact.to_user,
        ),
        theme=theme,
        seen_at=secret_text_message.seen_at,
        deleted_at=secret_text_message.deleted_at,
        created_at=secret_text_message.created_at,
    )


def get_contacts_secret_messages(
        contact_ids: Iterable[int],
) -> list[ContactSecretTextMessageDTO]:
    secret_messages = (
        SecretTextMessage.objects
        .select_related('contact')
        .filter(contact_id__in=contact_ids, deleted_at__isnull=True)
        .order_by('created_at')
        .values(
            'id',
            'text',
            'contact__of_user_id',
            'contact__to_user_id',
            'seen_at',
            'created_at',
        )
    )

    return [
        ContactSecretTextMessageDTO(
            id=secret_message['id'],
            text=secret_message['text'],
            sender_id=secret_message['contact__of_user_id'],
            recipient_id=secret_message['contact__to_user_id'],
            seen_at=secret_message['seen_at'],
            created_at=secret_message['created_at'],
        )
        for secret_message in secret_messages
    ]
