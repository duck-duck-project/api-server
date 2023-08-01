from django.contrib import admin

from secret_messages.models import SecretMessage, Contact


@admin.register(SecretMessage)
class SecretMessageAdmin(admin.ModelAdmin):
    pass


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    pass