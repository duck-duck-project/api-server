from datetime import timedelta

import humanize

from views.base import View

__all__ = ('TimeBeforeStudiesStartCountdownView',)


class TimeBeforeStudiesStartCountdownView(View):

    def __init__(
            self,
            *,
            time_before_studies_start: timedelta,
            urgency_coefficient: int,
    ):
        self.__time_before_studies_start = time_before_studies_start
        self.__urgency_coefficient = urgency_coefficient

    def get_text(self) -> str:
        humanized_time_before_studies_start = humanize.naturaldelta(
            self.__time_before_studies_start,
        )
        line = ''
        is_skull = True
        for _ in range(self.__urgency_coefficient):
            line += '💀' if is_skull else '🔥'
            is_skull = not is_skull
        return (
            f'{line}\n'
            f'До начала учебы {humanized_time_before_studies_start}\n'
            f'{line}'
        )
