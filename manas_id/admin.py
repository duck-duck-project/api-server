from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from manas_id.models import ManasId, Department, Country, Region, Nationality


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
    list_filter = ('department', 'course', 'gender')
    autocomplete_fields = ('user', 'department', 'region', 'nationality')
    ordering = ('-created_at',)
    list_select_related = ('department',)
    search_fields = ('first_name', 'last_name', 'student_id', 'user_id')
    search_help_text = 'Search by name, student ID, user ID'
