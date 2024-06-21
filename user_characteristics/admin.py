from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from user_characteristics.models import (
    FoodItem,
    FoodItemAlias,
    Medicine,
    SportActivity,
    SportActivityAction,
)


class FoodItemAliasInline(admin.TabularInline):
    model = FoodItemAlias
    autocomplete_fields = ('food_item',)
    fields = ('name', 'food_item')
    show_change_link = True


@admin.register(FoodItemAlias)
class FoodItemAliasAdmin(ImportExportModelAdmin):
    list_display = ('food_item', 'name',)
    list_select_related = ('food_item',)
    search_fields = ('name', 'food_item__name')
    search_help_text = 'Search by food item name or alias name'
    autocomplete_fields = ('food_item',)


@admin.register(SportActivity)
class SportActivityAdmin(ImportExportModelAdmin):
    list_display = (
        'name',
        'emoji',
        'energy_cost_value',
        'health_benefit_value',
        'cooldown_in_seconds',
    )


@admin.register(FoodItem)
class FoodItemAdmin(ImportExportModelAdmin):
    list_display = (
        'name',
        'emoji',
        'type',
        'price',
        'energy_benefit_value',
        'health_impact_value',
    )
    list_filter = ('type',)
    search_fields = ('name',)
    search_help_text = 'Search by name'
    inlines = (FoodItemAliasInline,)


@admin.register(Medicine)
class MedicineAdmin(ImportExportModelAdmin):
    list_display = ('name', 'emoji', 'price', 'health_benefit_value')
    search_fields = ('name',)
    search_help_text = 'Search by name'


@admin.register(SportActivityAction)
class SportActivityActionAdmin(ImportExportModelAdmin):
    pass
