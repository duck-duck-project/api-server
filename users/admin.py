from django.contrib import admin

from users.models import User, Contact, Preferences

__all__ = (
    'UserAdmin',
    'ContactAdmin',
    'PreferencesAdmin',
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    pass


@admin.register(Preferences)
class PreferencesAdmin(admin.ModelAdmin):
    pass
