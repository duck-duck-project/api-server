from typing import Any

from drf_standardized_errors.formatter import ExceptionFormatter
from drf_standardized_errors.types import ErrorResponse
from rest_framework.exceptions import APIException


class ApplicationError(Exception):
    """
    Base class for all exceptions which are raised by the application.
    But not API layer.
    """


def validate_error_code(error: str) -> None:
    if ' ' in error:
        raise ApplicationError('Error code must not contain spaces.')
    if not error.islower():
        raise ApplicationError('Error code must be in lower case.')


def create_api_error(
        error: str,
        status_code: int,
        extra: dict[str, Any] | None = None,
) -> APIException:
    """
    APIException factory.

    Args:
        error: short error code.
        status_code: HTTP response status code.
        extra: extra info in response.

    Returns:
        APIException instance.
    """
    validate_error_code(error)
    data = {'error': error, 'ok': False}
    if extra is not None:
        data['extra'] = extra
    error = APIException(data)
    error.status_code = status_code
    return error


class CustomFormatter(ExceptionFormatter):

    def format_error_response(self, error_response: ErrorResponse) -> Any:
        extra: dict | None = getattr(self.exc, 'extra', None)

        error_response = super().format_error_response(error_response)
        for error in error_response['errors']:
            if extra is not None and error['code'] == self.exc.default_code:
                error['extra'] = extra

        return error_response
