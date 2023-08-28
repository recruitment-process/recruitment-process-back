from django.conf import settings
from django.core.mail import send_mail
from rest_framework import serializers
from telegram import Bot, TelegramError


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


def send_mail_to_user(email, confirmation_code):
    """Отправка кода подтверждения на почту."""
    message = (
        "Подтвердить почту перейдя по ссылке: "
        f"http://localhost:8000/confirm/{email}/{confirmation_code}"
    )
    #    message = ("Подтвердить почту перейдя по ссылке: "
    #               f"http://80.87.107.166/confirm/{email}/{confirmation_code}")
    send_mail(
        "Подтверждение регистрации в Meeting Room",
        message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
    bot = Bot(token=settings.TELEGRAM_TOKEN)
    try:
        bot.send_message(settings.TELEGRAM_CHAT_ID, message)
    except TelegramError as error:
        print(error)
