from django.conf import settings
from django.contrib import admin

from economics.models import Transaction
from telegram.services import (
    closing_telegram_http_client_factory,
    TelegramBotService,
    TransactionNotifier,
)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    search_fields = ('id',)
    search_help_text = 'Search by ID'
    sortable_by = ('amount', 'created_at')
    list_display = ('sender', 'recipient', 'amount', 'source', 'created_at')
    list_display_links = ('sender', 'recipient')
    list_per_page = 20
    ordering = ('-created_at',)
    list_filter = ('source',)
    empty_value_display = 'System'
    autocomplete_fields = ('sender', 'recipient')

    def save_model(self, request, obj: Transaction, form, change):
        super().save_model(request, obj, form, change)

        with closing_telegram_http_client_factory(
                token=settings.TELEGRAM_BOT_TOKEN,
        ) as http_client:
            telegram_bot_service = TelegramBotService(http_client)
            transaction_notifier = TransactionNotifier(telegram_bot_service)

            if obj.is_deposit:
                transaction_notifier.notify_deposit(obj)
            elif obj.is_withdrawal:
                transaction_notifier.notify_withdrawal(obj)
