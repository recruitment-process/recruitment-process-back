from django.conf import settings
from django.core.mail import send_mail
from telegram import Bot, TelegramError


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
