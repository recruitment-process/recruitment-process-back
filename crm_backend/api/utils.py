from rest_framework import serializers


class DateOnlyField(serializers.DateTimeField):
    """Класс преобразования формата даты.."""

    def to_representation(self, value):
        """Функция преобразования вывода формата даты."""
        return value.strftime("%Y-%m-%d")


def get_display_values(keys, choices):
    """Функция преобразования вывода информации для поля с ключа на значение."""
    if keys:
        display_values = [dict(choices).get(key) for key in keys]
        return display_values
    return None
