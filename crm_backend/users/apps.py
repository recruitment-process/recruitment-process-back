from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Модель Юзер."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "users"
