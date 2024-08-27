from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException


class SportActivityDoesNotExistError(Exception):

    def __init__(self, sport_activity_name: str):
        super().__init__('Sport activity does not exist')
        self.sport_activity_name = sport_activity_name


class MedicineDoesNotExistError(Exception):

    def __init__(self, medicine_name: str):
        super().__init__('Medicine does not exist')
        self.medicine_name = medicine_name


class FoodItemNotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = _('Food item was not found.')
    default_code = 'food_item_not_found'

    def __init__(self, food_item_name: str, food_item_type: int):
        super().__init__()
        self.extra = {
            'food_item_name': food_item_name,
            'food_item_type': food_item_type,
        }


class SportActivityCooldownError(Exception):

    def __init__(self, cooldown_in_seconds: int, next_activity_in_seconds: int):
        super().__init__('Sport activity is on cooldown')
        self.cooldown_in_seconds = cooldown_in_seconds
        self.next_activity_in_seconds = next_activity_in_seconds
