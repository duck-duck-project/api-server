from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from economics.models import Transaction
from economics.services import compute_user_balance
from users.models import User, Contact, Team, TeamMember

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
                source=Transaction.Source.SYSTEM,
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


class TeamMemberInline(admin.TabularInline):
    model = TeamMember
    extra = 0


@admin.register(Team)
class TeamAdmin(ImportExportModelAdmin):
    inlines = (TeamMemberInline,)


@admin.register(TeamMember)
class TeamMemberAdmin(ImportExportModelAdmin):
    list_filter = ('team',)
    list_select_related = ('team',)
    list_display = ('team', 'user')
