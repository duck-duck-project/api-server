from django.contrib import admin
from fast_depends import inject, Depends

from economics.dependencies import get_transaction_notifier
from economics.models import Transaction
from telegram.services import TransactionNotifier


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    search_fields = ('id',)
    search_help_text = 'Search by ID'
    sortable_by = ('amount', 'created_at')
    list_display = ('sender', 'recipient', 'amount', 'created_at')
    list_display_links = ('sender', 'recipient')
    list_per_page = 20
    ordering = ('-created_at',)
    empty_value_display = 'System'
    autocomplete_fields = ('sender', 'recipient')

    @inject
    def save_model(
            self,
            request,
            obj: Transaction,
            form,
            change,
            transaction_notifier: TransactionNotifier = (
                    Depends(get_transaction_notifier)
            ),
    ):
        super().save_model(request, obj, form, change)

        if obj.is_deposit:
            transaction_notifier.notify_deposit(obj)
        elif obj.is_withdrawal:
            transaction_notifier.notify_withdrawal(obj)
