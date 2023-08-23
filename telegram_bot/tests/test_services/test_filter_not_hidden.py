from dataclasses import dataclass

from services import filter_not_hidden


@dataclass(frozen=True)
class HasIsHidden:
    is_hidden: bool


def test_filter_not_hidden():
    items = [HasIsHidden(is_hidden=True), HasIsHidden(is_hidden=False)]
    assert filter_not_hidden(items) == [HasIsHidden(is_hidden=False)]
