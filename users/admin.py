from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from economics.models import Transaction
from economics.services import compute_user_balance
from users.models import Contact, Tag, Theme, User

__all__ = (
    'UserAdmin',
    'ContactAdmin',
    'Theme',
)


class ThemeResource(resources.ModelResource):
    class Meta:
        model = Theme


class UserResource(resources.ModelResource):
    class Meta:
        model = User


class ContactResource(resources.ModelResource):
    class Meta:
        model = Contact


@admin.register(Theme)
class ThemeAdmin(ImportExportModelAdmin):
    resource_class = ThemeResource
    ordering = ('-created_at',)
    list_display = ('__str__',)
    list_filter = ('is_hidden',)


@admin.register(User)
class UserAdmin(ImportExportModelAdmin):
    resource_class = UserResource
    search_fields = ('username', 'fullname', 'id')
    readonly_fields = ('id', 'view_balance')
    list_filter = ('can_be_added_to_contacts', 'is_banned')
    list_display = ('username', 'fullname')
    ordering = ('-created_at',)
    actions = ('deposit_balance',)

    @admin.display(description='Balance')
    def view_balance(self, user: User):
        return str(compute_user_balance(user))

    @admin.action(description='Deposit balance for $1000')
    def deposit_balance(
            self,
            _: HttpRequest,
            queryset: QuerySet[User],
    ) -> None:
        transactions = [
            Transaction(
                recipient=user,
                amount=1000,
            ) for user in queryset
        ]
        Transaction.objects.bulk_create(transactions)


@admin.register(Contact)
class ContactAdmin(ImportExportModelAdmin):
    resource_class = ContactResource
    search_fields = (
        'of_user__username',
        'of_user__fullname',
        'to_user__username',
        'to_user__fullname',
    )
    list_filter = ('of_user', 'to_user', 'is_hidden')
    list_select_related = ('of_user', 'to_user')
    list_display = ('of_user', 'to_user', 'private_name', 'public_name')
    list_display_links = ('of_user', 'to_user')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_filter = ('weight',)
    list_display = ('text', 'weight', 'of_user', 'to_user')
    list_select_related = ('of_user', 'to_user')
