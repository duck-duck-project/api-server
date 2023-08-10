from django.contrib import admin

from secret_messages.models.secret_medias import SecretMedia
from secret_messages.models.secret_message_templates import (
    SecretMessageDescriptionTemplate,
    SecretMessageButtonTemplate,
)
from secret_messages.models.secret_messages import SecretMessage


@admin.register(SecretMessageDescriptionTemplate)
class SecretMessageDescriptionTemplateAdmin(admin.ModelAdmin):
    pass


@admin.register(SecretMessageButtonTemplate)
class SecretMessageButtonTemplateAdmin(admin.ModelAdmin):
    pass


@admin.register(SecretMessage)
class SecretMessageAdmin(admin.ModelAdmin):
    pass


@admin.register(SecretMedia)
class SecretMediaAdmin(admin.ModelAdmin):
    pass
