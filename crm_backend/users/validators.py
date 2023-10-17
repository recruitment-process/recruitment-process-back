import re

from django.core.exceptions import ValidationError


def custom_validate_email(value):
    """Кастомная валидация email для соответствия с валидацией frontend'а."""
    if not re.fullmatch(r"^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]{1,}\.[a-zA-Z]{2,}$", value):
        raise ValidationError("Введите правильный адрес электронной почты.")
    return value


class CustomPasswordValidator:
    """Кастомная валидация пароля для соответствия с валидацией frontend'а."""

    def validate(self, password, user=None):
        """Проверка пароля на соответствие."""
        if len(password) < 8 or len(password) > 128:
            raise ValidationError(
                "Минимальная длина пароля 8 символов, максимальная 128!"
            )
        if not re.match(r"^[^\sа-яА-Я]+$", password):
            raise ValidationError(
                "Пароль не должен содержать невидимые символы и кириллицу!"
            )

    def get_help_text(self):
        """Подсказка."""
        return (
            "Пароль не должен содержать невидимые символы и кириллицу,"
            " длина от 8 до 128 символов."
        )
