from django.contrib import admin

from relationships.models import Relationship, RelationshipStarsTransaction


@admin.register(Relationship)
class RelationshipAdmin(admin.ModelAdmin):
    list_display = ('first_user', 'second_user', 'created_at', 'broke_up_at')


@admin.register(RelationshipStarsTransaction)
class RelationshipStarsTransactionAdmin(admin.ModelAdmin):
    list_display = ('relationship', 'amount', 'description', 'created_at')
    list_filter = ('relationship', 'created_at')
    search_fields = ('description',)
