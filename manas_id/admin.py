from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from manas_id.models import ManasId, Department


class DepartmentResource(resources.ModelResource):

    class Meta:
        model = Department


@admin.register(Department)
class DepartmentAdmin(ImportExportModelAdmin):
    resource_class = DepartmentResource
    list_display = ('name',)


@admin.register(ManasId)
class ManasIdAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'department',
    )
    list_filter = ('department', 'course', 'gender')
