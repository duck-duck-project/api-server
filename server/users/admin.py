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
    search_fields = ('username', 'fullname', 'id')
    list_filter = ('is_premium', 'can_be_added_to_contacts')


@admin.register(Contact)
class ContactAdmin(ImportExportModelAdmin):
    resource_class = ContactResource
    search_fields = (
        'of_user__username',
        'of_user__fullname',
        'to_user__username',
        'to_user__fullname',
    )
    list_filter = ('of_user', 'is_hidden')
    list_select_related = ('of_user', 'to_user')
    list_display = ('of_user', 'to_user', 'private_name', 'public_name')
    list_display_links = ('of_user', 'to_user')
