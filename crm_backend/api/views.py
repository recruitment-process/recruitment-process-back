from django.conf import settings
from django.contrib.auth import authenticate
from django.middleware import csrf
from django_filters.rest_framework import DjangoFilterBackend
from recruitment.models import ApplicantResume, Vacancy
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    ResumeSerializer,
    ResumesSerializer,
    VacanciesSerializer,
    VacancySerializer,
)


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


class VacancyViewSet(ModelViewSet):
    """Вьюсет для модели вакансий."""

    queryset = Vacancy.objects.all()
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )
    filterset_fields = (
        "vacancy_title",
        "author",
        "company",
        "required_experience",
        "employment_type",
        "schedule_work",
        "salary",
        "city",
        "pub_date",
        "status",
        "technology_stack",
        "deadline",
    )
    search_fields = (
        "vacancy_title",
        "company__company_title",
        "city",
        "technology_stack",
    )
    ordering_fields = (
        "status",
        "deadline",
        "pub_date",
    )
    ordering = ("pub_date",)

    def get_serializer_class(self):
        """Функция определяющая сериализатор в зависимости от действия."""
        if self.action == "list":
            return VacanciesSerializer
        return VacancySerializer

    def perform_create(self, serializer):
        """Переопределение метода create для записи информация о пользователе."""
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        """Переопределение метода update для записи информация о пользователе."""
        serializer.save(author=self.request.user)


class ResumeViewSet(ModelViewSet):
    """Вьюсет для модели резюме."""

    queryset = ApplicantResume.objects.all()
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )
    filterset_fields = (
        "job_title",
        "employment_type",
        "schedule_work",
        "salary",
        "working_trip",
        "relocation",
        "gender",
        "pub_date",
        "education",
        "town",
        "citizenship",
        "bday",
        "work_experiences",
        "interview_status",
    )
    search_fields = (
        "job_title",
        "town",
        "current_job",
    )
    ordering_fields = (
        "applicant",
        "work_experiences",
        "interview_status",
        "current_company",
        "pub_date",
    )
    ordering = ("pub_date",)

    def get_serializer_class(self):
        """Функция определяющая сериализатор в зависимости от действия."""
        if self.action == "list":
            return ResumesSerializer
        return ResumeSerializer
