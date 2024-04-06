from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export.resources import ModelResource

from wishes.models import Wish


class WishResource(ModelResource):
    class Meta:
        model = Wish


@admin.register(Wish)
class WishAdmin(ImportExportModelAdmin):
    resource_class = WishResource
    search_fields = ('text',)
    list_display = ('__str__',)
