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
    autocomplete_fields = ('user', 'department')
    ordering = ('-created_at',)
    list_select_related = ('department',)
    search_fields = ('first_name', 'last_name', 'student_id', 'user_id')
    search_help_text = 'Search by name, student ID, user ID'
