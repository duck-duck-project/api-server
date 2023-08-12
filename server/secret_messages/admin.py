from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from secret_messages.models.secret_medias import SecretMedia
from secret_messages.models.secret_message_themes import SecretMessageTheme
from secret_messages.models.secret_messages import SecretMessage


class SecretMessageThemeResource(resources.ModelResource):

    class Meta:
        model = SecretMessageTheme


class SecretMessageResource(resources.ModelResource):

    class Meta:
        model = SecretMessage


class SecretMediaResource(resources.ModelResource):

    class Meta:
        model = SecretMedia


@admin.register(SecretMessageTheme)
class SecretMessageThemeAdmin(ImportExportModelAdmin):
    resource_class = SecretMessageThemeResource


@admin.register(SecretMessage)
class SecretMessageAdmin(ImportExportModelAdmin):
    resource_class = SecretMessageResource


@admin.register(SecretMedia)
class SecretMediaAdmin(ImportExportModelAdmin):
    resource_class = SecretMediaResource
