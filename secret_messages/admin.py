from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from secret_messages.models.secret_medias import SecretMedia
from secret_messages.models.secret_messages import SecretTextMessage


class SecretTextMessageResource(resources.ModelResource):
    class Meta:
        model = SecretTextMessage


class SecretMediaResource(resources.ModelResource):
    class Meta:
        model = SecretMedia


@admin.register(SecretTextMessage)
class SecretMessageAdmin(ImportExportModelAdmin):
    resource_class = SecretTextMessageResource
    ordering = ('-created_at',)
    list_display = ('id', 'created_at', 'text')
    sortable_by = ('created_at',)
    search_fields = ('text',)
    search_help_text = 'Search by text content'
    date_hierarchy = 'created_at'


@admin.register(SecretMedia)
class SecretMediaAdmin(ImportExportModelAdmin):
    resource_class = SecretMediaResource
    list_filter = ('contact', 'media_type')
    list_display = ('id', 'media_type', 'contact')
    ordering = ('-created_at',)
