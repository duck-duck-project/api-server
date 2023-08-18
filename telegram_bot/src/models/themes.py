from typing import Annotated

from pydantic import AfterValidator, BaseModel

__all__ = (
    'SecretMessageTheme',
    'contains_name_placeholder',
    'ContainsNamePlaceholder',
)


def contains_name_placeholder(text: str) -> str:
    assert '{name}' in text
    return text


ContainsNamePlaceholder = Annotated[
    str,
    AfterValidator(contains_name_placeholder)
]


class SecretMessageTheme(BaseModel):
    id: int
    description_template_text: ContainsNamePlaceholder
    button_text: str
