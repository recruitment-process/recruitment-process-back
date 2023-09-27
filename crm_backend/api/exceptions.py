from drf_standardized_errors.formatter import ExceptionFormatter
from drf_standardized_errors.types import ErrorResponse


class MyExceptionFormatter(ExceptionFormatter):
    """
    Класс для форматирования исключений.

    Наследует ExceptionFormatter и переопределяет метод format_error_response.
    """

    def format_error_response(self, error_response: ErrorResponse):
        """
        Метод принимает объект ErrorResponse и форматирует его.

        Возвращает словарь с ключами "success", "type", "code", "fieldname" и "message".
        """
        error = error_response.errors[0]
        return {
            "success": False,
            "type": error_response.type,
            "code": error.code,
            "field_name": error.attr,
            "message": error.detail,
        }
