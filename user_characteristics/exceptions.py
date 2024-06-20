class SportActivityDoesNotExistError(Exception):

    def __init__(self, sport_activity_name: str):
        super().__init__('Sport activity does not exist')
        self.sport_activity_name = sport_activity_name


class MedicineDoesNotExistError(Exception):

    def __init__(self, medicine_name: str):
        super().__init__('Medicine does not exist')
        self.medicine_name = medicine_name
