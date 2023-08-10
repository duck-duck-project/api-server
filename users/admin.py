from django.contrib import admin

from users.models import User, Contact

__all__ = ('UserAdmin',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    pass
