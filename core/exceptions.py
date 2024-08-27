from typing import Any

from drf_standardized_errors.formatter import ExceptionFormatter
from drf_standardized_errors.types import ErrorResponse

__all__ = ('CustomFormatter',)


class CustomFormatter(ExceptionFormatter):

    def format_error_response(self, error_response: ErrorResponse) -> Any:
        extra: dict | None = getattr(self.exc, 'extra', None)

        error_response = super().format_error_response(error_response)
        for error in error_response['errors']:
            if extra is not None and error['code'] == self.exc.default_code:
                error['extra'] = extra

        return error_response
