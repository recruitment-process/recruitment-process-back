from django.conf import settings
from django.contrib.auth import authenticate
from django.middleware import csrf
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User

from .serializers import UserSignupSerializer
from .utils import send_mail_to_user


def get_tokens_for_user(user):
    """Получение токенов для пользователя."""
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class LoginView(APIView):
    """Аутентификация пользователя."""

    permission_classes = [AllowAny]

    def post(self, request, format=None):
        """POST запрос на получение токенов."""
        data = request.data
        response = Response()
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                data = get_tokens_for_user(user)
                response.set_cookie(
                    key=settings.SIMPLE_JWT["AUTH_COOKIE"],
                    value=data["access"],
                    expires=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
                    secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                    httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                    samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
                )
                csrf.get_token(request)
                response.data = {"Success": "Login successfully", "data": data}
                return response
            else:
                return Response(
                    {"No active": "This account is not active!!"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(
                {"Invalid": "Invalid email or password!!"},
                status=status.HTTP_404_NOT_FOUND,
            )


class UserSignupView(APIView):
    """Регистрация пользователя."""

    pagination_class = None
    permission_classes = [AllowAny]

    def post(self, request):
        """POST запрос создания пользователя."""
        serializer = UserSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        send_mail_to_user(user.email, user.confirmation_code)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class EmailConfirmationView(APIView):
    """Подтверждение email пользователя."""

    pagination_class = None
    permission_classes = [AllowAny]

    def get(self, request, email, confirmation_code):
        """GET запрос подтверждения email."""
        user = get_object_or_404(User, email=email)
        if user.confirmation_code == confirmation_code:
            user.email_status = True
            user.save()
            return Response({"Email подтвержден!"}, status=status.HTTP_200_OK)
        return Response({"Неверная ссылка!"}, status=status.HTTP_400_BAD_REQUEST)
