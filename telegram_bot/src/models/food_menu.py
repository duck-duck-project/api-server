from pydantic import BaseModel, HttpUrl

__all__ = ('FoodMenuItem',)


class FoodMenuItem(BaseModel):
    name: str
    calories: int
    image_url: HttpUrl
