from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export.resources import ModelResource

from holidays.models import Holiday

__all__ = ('HolidayAdmin',)


class HolidayResource(ModelResource):
    class Meta:
        model = Holiday


@admin.register(Holiday)
class HolidayAdmin(ImportExportModelAdmin):
    resource_class = HolidayResource
    search_fields = ('name',)
    list_display = ('name',)
    list_filter = ('month', 'day')
