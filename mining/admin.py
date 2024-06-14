from django.contrib import admin

from mining.models import MiningAction


@admin.register(MiningAction)
class MiningActionAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'resource_name',
        'wealth',
        'created_at',
        'next_mining_at',
    )
    list_filter = ('resource_name',)
    list_select_related = ('user',)
