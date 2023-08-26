import telebot
from django.conf import settings
from django.core.mail import send_mail

bot = telebot.TeleBot(settings.TELEGRAM_TOKEN)


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
    send_to_telegram(settings.TELEGRAM_CHAT_ID, message, 12)


def send_to_telegram(chat_id, message, thread_id=None):
    """Отправка сообщения в телеграмм."""
    try:
        bot.send_message(chat_id, message, message_thread_id=thread_id)
    except Exception as e:
        print(e)
