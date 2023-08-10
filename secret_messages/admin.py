from django.contrib import admin

from secret_messages.models.contacts import Contact
from secret_messages.models.secret_medias import SecretMedia
from secret_messages.models.secret_messages import SecretMessage


@admin.register(SecretMessage)
class SecretMessageAdmin(admin.ModelAdmin):
    pass


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    pass


@admin.register(SecretMedia)
class SecretMediaAdmin(admin.ModelAdmin):
    pass
