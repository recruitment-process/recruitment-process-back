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


def get_salary_expectations(obj):
    """
    Функция для изменения представления поля salary_expectations.

    Приведено к виду salary_expectations: {min: 50, max: 66}.
    """
    if obj.salary_expectations:
        return {
            "min": obj.salary_expectations[0],
            "max": obj.salary_expectations[1],
        }
    return None


def get_salary_range(obj):
    """
    Функция для изменения представления поля salary.

    Приведено к виду salary: {min: 50, max: 66}.
    """
    if obj.salary:
        return {
            "min": obj.salary[0],
            "max": obj.salary[1],
        }
    return None
