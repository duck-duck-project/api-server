from django.contrib import admin
from django.forms import ModelForm
from django.http import HttpRequest
from fast_depends import Depends, inject
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from economics.dependencies import get_transaction_notifier
from economics.services import create_system_deposit
from manas_id.models import ManasId, Department, Country, Region, Nationality
from telegram.services import TransactionNotifier


class NationalityResource(resources.ModelResource):

    class Meta:
        model = Nationality


class CountryResource(resources.ModelResource):

    class Meta:
        model = Country


class RegionResource(resources.ModelResource):

    class Meta:
        model = Region


class DepartmentResource(resources.ModelResource):

    class Meta:
        model = Department


@admin.register(Nationality)
class NationalityAdmin(ImportExportModelAdmin):
    resource_class = NationalityResource
    list_display = ('__str__',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Country)
class CountryAdmin(ImportExportModelAdmin):
    resource_class = CountryResource
    list_display = ('__str__',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Region)
class RegionAdmin(ImportExportModelAdmin):
    resource_class = RegionResource
    list_display = ('name', 'country')
    list_filter = ('country',)
    list_select_related = ('country',)
    search_fields = ('name',)
    ordering = ('name',)
    autocomplete_fields = ('country',)


@admin.register(Department)
class DepartmentAdmin(ImportExportModelAdmin):
    resource_class = DepartmentResource
    list_display = ('__str__', 'code')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(ManasId)
class ManasIdAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'department',
        'created_at',
    )
    list_filter = (
        'department',
        'course',
        'gender',
        'region',
        'nationality',
        'region__country',
    )
    autocomplete_fields = ('user', 'department', 'region', 'nationality')
    ordering = ('-created_at',)
    list_select_related = ('department', 'region', 'region__country')
    search_fields = ('first_name', 'last_name', 'student_id', 'user_id')
    search_help_text = 'Search by name, student ID, user ID'

    @inject
    def save_model(
            self,
            request: HttpRequest,
            obj: ManasId,
            form: ModelForm,
            change: bool,
            transaction_notifier: TransactionNotifier = Depends(
                get_transaction_notifier,
            ),
    ):
        super().save_model(request, obj, form, change)

        is_created = not change
        if is_created:
            deposit = create_system_deposit(
                user=obj.user,
                amount=50000,
                description='Регистрация Manas ID',
            )
            transaction_notifier.notify_deposit(deposit)
