from django.contrib import admin

from secret_messages.models.secret_medias import SecretMedia
from secret_messages.models.secret_messages import SecretMessage
from secret_messages.models.secret_message_themes import SecretMessageTheme


@admin.register(SecretMessageTheme)
class SecretMessageThemeAdmin(admin.ModelAdmin):
    pass


@admin.register(SecretMessage)
class SecretMessageAdmin(admin.ModelAdmin):
    pass


@admin.register(SecretMedia)
class SecretMediaAdmin(admin.ModelAdmin):
    pass
