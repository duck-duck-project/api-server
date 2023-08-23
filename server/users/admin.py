from datetime import timedelta

from django.contrib import admin
from django.db.models import QuerySet, Q
from django.http import HttpRequest
from django.utils import timezone
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from users.models import User, Contact

__all__ = (
    'UserAdmin',
    'ContactAdmin',
)


class IsPremiumListFilter(admin.SimpleListFilter):
    title = 'Is premium'

    parameter_name = 'is_premium'

    def lookups(self, request: HttpRequest, model_admin: 'UserAdmin'):
        return [
            ('1', 'Yes'),
            ('0', 'No'),
        ]

    def queryset(self, request: HttpRequest, queryset: QuerySet[User]):
        threshold_30_days_before = timezone.now() - timedelta(days=30)
        if self.value() == '1':
            queryset = queryset.filter(
                subscription_started_at__isnull=False,
                subscription_started_at__gte=threshold_30_days_before,
            )
        if self.value() == '0':
            queryset = queryset.filter(
                Q(subscription_started_at__isnull=True)
                | Q(
                    subscription_started_at__isnull=False,
                    subscription_started_at__lt=threshold_30_days_before,
                )
            )
        return queryset


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
    readonly_fields = ('id', 'view_is_premium')
    list_filter = (IsPremiumListFilter, 'can_be_added_to_contacts', 'is_banned')
    list_display = ('username', 'fullname', 'view_is_premium')
    ordering = ('-created_at',)

    @admin.display(description='Is premium', boolean=True)
    def view_is_premium(self, user: User):
        return user.is_premium


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
