from django.conf import settings
from django.db import transaction, IntegrityError

from economics.models import OperationPrice
from economics.services import create_system_withdrawal
from telegram.services import (
    TransactionNotifier,
    TelegramBotService,
    closing_telegram_http_client_factory,
)
from users.exceptions import ContactAlreadyExistsError
from users.models import User, Contact

__all__ = (
    'create_contact',
    'update_contact',
    'delete_contact_by_id',
)


@transaction.atomic
def create_contact(
        *,
        of_user: User,
        to_user: User,
        private_name: str,
        public_name: str,
) -> Contact:
    """Create contact. If soft deleted, mark it as not deleted.
    Withdraw funds from user for contact creation.

    Keyword Args:
        of_user: user that owns contact.
        to_user: user that is contact.
        private_name: name of contact that is visible only to user.
        public_name: name of contact that is visible to all users.

    Returns:
        Contact instance.

    Raises:
        InsufficientFundsForSystemWithdrawalError:
            if user does not have enough funds for contact creation.
    """
    try:
        contact = Contact.objects.get(of_user=of_user, to_user=to_user)
    except Contact.DoesNotExist:
        contact = Contact.objects.create(
            of_user=of_user,
            to_user=to_user,
            private_name=private_name,
            public_name=public_name,
        )
    else:
        if contact.is_deleted:
            contact.is_deleted = False
            contact.save()
        else:
            raise ContactAlreadyExistsError

    withdrawal = create_system_withdrawal(
        user=of_user,
        amount=OperationPrice.CREATE_CONTACT,
        description='Добавление в контакты контакта'
    )

    with closing_telegram_http_client_factory(
            token=settings.TELEGRAM_BOT_TOKEN,
    ) as telegram_http_client:
        telegram_bot_service = TelegramBotService(telegram_http_client)
        transaction_notifier = TransactionNotifier(telegram_bot_service)
        transaction_notifier.notify_withdrawal(withdrawal)

    return contact


def update_contact(
        *,
        contact_id: int,
        private_name: str,
        public_name: str,
        is_hidden: bool,
) -> bool:
    """Update contact.

    Keyword Args:
        contact_id: id of contact to update.
        private_name: name of contact that is visible only to user.
        public_name: name of contact that is visible to all users.
        is_hidden: whether contact is hidden from user.
    """
    updated_count = Contact.objects.filter(id=contact_id).update(
        private_name=private_name,
        public_name=public_name,
        is_hidden=is_hidden,
    )
    return bool(updated_count)


def delete_contact_by_id(contact_id: int) -> bool:
    """Soft delete contact by id.

    Keyword Args:
        contact_id: id of contact to delete.

    Returns:
        True if contact was marked as deleted, False otherwise.
    """
    deleted_count = (
        Contact
        .objects
        .filter(id=contact_id)
        .update(is_deleted=True)
    )
    return bool(deleted_count)
