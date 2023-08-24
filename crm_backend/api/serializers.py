import re

from rest_framework import serializers
from users.models import User
from users.validators import custom_validate_email


class UserSignupSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя при регистрации."""

    password = serializers.CharField(max_length=255)
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = (
            "email",
            "password",
        )

    def create(self, validated_data):
        """Создание пользователя в БД."""
        user = User.objects.create_user(
            validated_data["email"], validated_data["password"]
        )
        return user

    def validate_email(self, value):
        """Валидация email."""
        return custom_validate_email(value)

    def validate_password(self, value):
        """Валидация пароля."""
        if len(value) < 8:
            raise serializers.ValidationError("Минимальная длина пароля 8 символов!")
        if not re.match(r"^[^\sа-яА-Я]+$", value):
            raise serializers.ValidationError(
                "Пароль не должен содержать невидимые символы и кириллицу!"
            )
        return value

    def validate(self, data):
        """Проверка на существование пользователя с email."""
        email = data.get("email")
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                f"Пользователь с адресом {email} уже существует"
            )
        return data
