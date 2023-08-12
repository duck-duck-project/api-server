from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from users.models import User, Contact

__all__ = (
    'UserAdmin',
    'ContactAdmin',
)


class UserResource(resources.ModelResource):

    class Meta:
        model = User


class ContactResource(resources.ModelResource):

    class Meta:
        model = Contact


@admin.register(User)
class UserAdmin(ImportExportModelAdmin):
    resource_class = UserResource


@admin.register(Contact)
class ContactAdmin(ImportExportModelAdmin):
    resource_class = ContactResource
