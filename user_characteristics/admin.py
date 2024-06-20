from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from user_characteristics.models import (
    FoodItem, Medicine, SportActivity, SportActivityAction,
)


@admin.register(SportActivity)
class SportActivityAdmin(ImportExportModelAdmin):
    pass


@admin.register(FoodItem)
class FoodItemAdmin(ImportExportModelAdmin):
    pass


@admin.register(Medicine)
class MedicineAdmin(ImportExportModelAdmin):
    pass


@admin.register(SportActivityAction)
class SportActivityActionAdmin(ImportExportModelAdmin):
    pass
