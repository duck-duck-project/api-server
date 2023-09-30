from django.contrib import admin

from economics.models import Transaction


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
