import re

from django.core.exceptions import ValidationError


def custom_validate_email(value):
    """Кастомная валидация email для соответствия с валидация frontend'а."""
    if not re.fullmatch(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", value):
        raise ValidationError("Введите правильный адрес электронной почты.")
