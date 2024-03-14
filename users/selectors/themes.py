from uuid import UUID

from django.db.models import QuerySet

from users.models import Theme

__all__ = ('get_visible_themes', 'get_theme_by_id')


def get_visible_themes() -> QuerySet[Theme]:
    return Theme.objects.exclude(is_hidden=True).order_by('-created_at')


def get_theme_by_id(theme_id: UUID) -> Theme:
    return Theme.objects.get(id=theme_id)
