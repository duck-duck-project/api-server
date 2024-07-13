from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from mining.models import MiningAction

class MiningActionResource(resources.ModelResource):
    class Meta:
        model = MiningAction


@admin.register(MiningAction)
class MiningActionAdmin(ImportExportModelAdmin):
    resource_class = MiningActionResource
    list_display = (
        'user',
        'resource_name',
        'value',
        'created_at',
    )
    list_filter = ('resource_name',)
    list_select_related = ('user',)
