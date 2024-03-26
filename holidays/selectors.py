from holidays.models import DateHolidays, Holiday

__all__ = ('get_date_holidays',)


def get_date_holidays(*, month: int, day: int) -> DateHolidays:
    holiday_names = list(
        Holiday.objects
        .filter(month=month, day=day)
        .values_list('name', flat=True)
    )
    return DateHolidays(month=month, day=day, holidays=holiday_names)
