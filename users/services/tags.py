from users.models import Tag

__all__ = ('delete_tag_by_id',)


def delete_tag_by_id(tag_id: int) -> bool:
    r = Tag.objects.filter(id=tag_id).delete()
    print(r)
    return r
