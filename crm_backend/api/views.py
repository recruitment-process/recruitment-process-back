from datetime import datetime

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.middleware import csrf
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import (  # OpenApiExample,; OpenApiParameter,
    extend_schema,
    extend_schema_view,
    inline_serializer,
)
from recruitment.models import (
    ApplicantResume,
    Candidate,
    Company,
    Education,
    FunnelStage,
    Note,
    Vacancy,
)
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import BooleanField, CharField, EmailField, IntegerField
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User

from .filters import CandidatesFilterSet, ResumeFilterSet, VacancyFilterSet
from .serializers import (
    CandidateSerializer,
    CandidatesSerializer,
    ChangePasswordSerializer,
    CommentSerializer,
    CompanySerializer,
    CompanyShortSerializer,
    EducationSerializer,
    FunnelDetailSerializer,
    FunnelSerializer,
    NoteDetailSerializer,
    NoteSerializer,
    ResumeSerializer,
    ResumesSerializer,
    SubStageSerializer,
    UserSerializer,
    UserSignupSerializer,
    VacanciesSerializer,
    VacancySerializer,
)
from .utils import send_mail_to_user


def get_tokens_for_user(user):
    """
    Функция для получения токенов доступа для пользователя.

    Аргументы:
    user -- экземпляр модели User, для которого необходимо получить токены.

    Возвращает:
    Словарь с токенами "refresh" и "access".
    """
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


@extend_schema_view(
    post=extend_schema(
        summary="Аутентификация пользователя",
        description="POST запрос для получения токенов доступа.",
        tags=["Аутентификация"],
        responses={
            200: inline_serializer(
                name="Response",
                fields={
                    "id": IntegerField(),
                    "data": inline_serializer(
                        name="Tokens",
                        fields={"refresh": CharField(), "access": CharField()},
                    ),
                },
            )
        },
        request=inline_serializer(
            name="Request",
            fields={
                "email": EmailField(),
                "password": CharField(),
                "remember_me": BooleanField(required=False),
            },
        ),
    )
)
class LoginView(APIView):
    """
    Представление для аутентификации пользователя.

    Разрешения:
    AllowAny -- доступ разрешен всем пользователям.
    """

    permission_classes = [AllowAny]

    def post(self, request, format=None):
        """
        POST запрос для получения токенов доступа.

        Аргументы:
        request -- объект запроса Django.
        format -- формат ответа (необязательный).

        Возвращает:
        Response с токенами доступа в случае успешной аутентификации.
        Response с сообщением об ошибке в случае неудачной аутентификации.
        """
        data = request.data
        response = Response()
        email = data.get("email", None)
        password = data.get("password", None)
        remember_me = data.get("remember_me", None)
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                expires = (
                    datetime.utcnow() + settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"]
                )
                if not remember_me:
                    request.session.set_expiry(0)
                    expires = settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"]
                data = get_tokens_for_user(user)
                response.set_cookie(
                    key=settings.SIMPLE_JWT["AUTH_COOKIE"],
                    value=data["access"],
                    expires=expires,
                    secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                    httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                    samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
                )
                login(request, user)
                csrf.get_token(request)
                response.data = {"id": user.id, "data": data}
                return response
            return Response(
                {"No active": "This account is not active!!"},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(
            {"Invalid": "Invalid email or password!!"},
            status=status.HTTP_404_NOT_FOUND,
        )


@extend_schema(tags=["Аутентификация"])
@extend_schema_view(
    post=extend_schema(
        summary="Регистрация пользователя",
        description="Создает нового пользователя и отправляет ему подтверждение.",
    ),
)
class UserSignupView(APIView):
    """
    Представление для регистрации пользователя.

    Разрешения:
    AllowAny -- доступ разрешен всем пользователям.
    """

    pagination_class = None
    permission_classes = [AllowAny]

    def post(self, request):
        """
        POST запрос для создания пользователя.

        Аргументы:
        request -- объект запроса Django.

        Возвращает:
        Response с данными пользователя в случае успешной регистрации.
        """
        serializer = UserSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        send_mail_to_user(user.id, user.confirmation_code, user.email)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Аутентификация"])
@extend_schema_view(
    post=extend_schema(
        summary="Выход из системы",
        description="Выходит из системы и удаляет cookie с токеном доступа.",
    ),
)
class LogoutView(APIView):
    """
    Представление для выхода пользователя из системы.

    Разрешения:
    IsAuthenticated -- доступ разрешен только аутентифицированным пользователям.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        POST запрос для выхода пользователя из системы.

        Аргументы:
        request -- объект запроса Django.

        Возвращает:
        HttpResponseRedirect на страницу входа в систему.
        """
        logout(request)
        response = HttpResponseRedirect(f"http://{settings.DOMAIN_NAME}/login/")
        response.delete_cookie(settings.SIMPLE_JWT["AUTH_COOKIE"])
        return response


@extend_schema_view(
    get=extend_schema(
        summary="Подтверждение email пользователя",
        description="GET запрос для подтверждения email пользователя.",
        tags=["Аутентификация"],
        responses={
            200: inline_serializer(
                name="Success",
                fields={
                    "status": CharField(),
                },
            ),
            400: inline_serializer(
                name="Error",
                fields={
                    "status": CharField(),
                },
            ),
        },
    )
)
class EmailConfirmationView(APIView):
    """
    Представление для подтверждения email пользователя.

    Разрешения:
    AllowAny -- доступ разрешен всем пользователям.
    """

    pagination_class = None
    permission_classes = [AllowAny]

    def get(self, request, user_id, confirmation_code):
        """GET запрос подтверждения email."""
        user = get_object_or_404(User, pk=user_id)
        if user.confirmation_code == confirmation_code:
            user.email_status = True
            user.save()
            return HttpResponseRedirect(f"http://{settings.DOMAIN_NAME}/login/")
        return Response(
            {"status": "Неверная ссылка!"}, status=status.HTTP_400_BAD_REQUEST
        )


@extend_schema_view(
    list=extend_schema(
        summary="Получить список пользователей",
        description="Получает список пользователей, которые не являются персоналом.",
        tags=["Users"],
    ),
)
class UserViewSet(ModelViewSet):
    """Вьюсет для модели пользователей."""

    queryset = User.objects.filter(is_staff=False)
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"
    lookup_value_regex = r"[0-9]+"
    http_method_names = [
        "get",
    ]


@extend_schema_view(
    put=extend_schema(
        summary="Смена пароля пользователя",
        description="PUT запрос для смены пароля пользователя.",
        tags=["Аутентификация"],
        responses={
            204: inline_serializer(
                name="Success",
                fields={
                    "status": CharField(),
                },
            ),
            400: inline_serializer(
                name="Error",
                fields={
                    "неверный текущий пароль.": CharField(),
                },
            ),
        },
    )
)
class ChangePasswordView(APIView):
    """Смена пароля пользователя."""

    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        """Получение объекта пользователя."""
        return self.request.user

    def put(self, request, *args, **kwargs):
        """PUT запрос мены пароля пользователя."""
        self.object = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            old_password = serializer.data.get("old_password")
            if not self.object.check_password(old_password):
                return Response(
                    {"old_password": "неверный текущий пароль."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            self.object.set_password(serializer.data.get("new_password_1"))
            self.object.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["Вакансии"])
@extend_schema_view(
    list=extend_schema(
        summary="Получить список вакансий",
        description="Получает список вакансий, созданных автором запроса.",
    ),
    create=extend_schema(
        summary="Создать новую вакансию",
        description="Создает новую вакансию от имени автора запроса.",
    ),
    retrieve=extend_schema(
        summary="Получить информацию о вакансии",
        description="Получает информацию о конкретной вакансии.",
    ),
    update=extend_schema(
        summary="Обновить информацию о вакансии",
        description="Обновляет информацию о конкретной вакансии.",
    ),
    partial_update=extend_schema(
        summary="Частично обновить информацию о вакансии",
        description="Частично обновляет информацию о конкретной вакансии.",
    ),
    destroy=extend_schema(
        summary="Удалить вакансию",
        description="Удаляет конкретную вакансию, созданную автором запроса.",
    ),
)
class VacancyViewSet(ModelViewSet):
    """Вьюсет для модели вакансий."""

    permission_classes = (IsAuthenticated,)
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )
    filterset_class = VacancyFilterSet
    search_fields = (
        "vacancy_title",
        "company__company_title",
        "city",
        "skill_stack",
    )
    ordering_fields = (
        "vacancy_status",
        "deadline",
        "pub_date",
    )
    ordering = ("pub_date",)

    def get_queryset(self):
        """Получаем вакансии автора запроса."""
        user = self.request.user
        return Vacancy.objects.filter(author=user)

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


@extend_schema(tags=["Резюме"])
@extend_schema_view(
    list=extend_schema(
        summary="Получить список вакансий",
        description="Возвращает список всех вакансий, доступных текущему пользователю.",
    ),
    create=extend_schema(
        summary="Создать новую вакансию",
        description="Создает новую вакансию и сохраняет ее в базу данных.",
    ),
    retrieve=extend_schema(
        summary="Получить детальную информацию о вакансии.",
        description="Возвращает детальную информацию о выбранной вакансии.",
    ),
    update=extend_schema(
        summary="Обновить существующую вакансию",
        description="Обновляет данные существующей вакансии.",
    ),
    partial_update=extend_schema(
        summary="Частично обновить существующую вакансию",
        description="Обновляет одно или несколько полей существующей вакансии.",
    ),
    destroy=extend_schema(
        summary="Удалить вакансию",
        description="Удаляет выбранную вакансию из базы данных.",
    ),
)
class ResumeViewSet(ModelViewSet):
    """
    Вьюсет для модели резюме.

    Разрешения:
    IsAuthenticated -- доступ разрешен только аутентифицированным пользователям.
    """

    permission_classes = (IsAuthenticated,)
    queryset = ApplicantResume.objects.all()
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )
    filterset_class = ResumeFilterSet
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


@extend_schema(tags=["Заметки"])
@extend_schema_view(
    list=extend_schema(
        summary="Получить список заметок",
        description="Возвращает список всех заметок на кандидата.",
    ),
    create=extend_schema(
        summary="Создать новую заметку",
        description="Создает новую заметку и сохраняет ее в базу данных.",
    ),
    retrieve=extend_schema(
        summary="Получить детали заметки",
        description="Возвращает детальную информацию о выбранной заметке.",
    ),
    update=extend_schema(
        summary="Обновить существующую заметку",
        description="Обновляет данные существующей заметки.",
    ),
    partial_update=extend_schema(
        summary="Частично обновить существующую заметку",
        description="Обновляет одно или несколько полей существующей заметки.",
    ),
    destroy=extend_schema(
        summary="Удалить заметку",
        description="Удаляет выбранную заметку из базы данных.",
    ),
)
class NoteViewSet(ModelViewSet):
    """
    Вьюсет для модели заметок.

    Разрешения:
    IsAuthenticated -- доступ разрешен только аутентифицированным пользователям.
    """

    permission_classes = (IsAuthenticated,)
    ordering = ("pub_date",)

    def get_serializer_class(self):
        """Функция определяющая сериализатор в зависимости от действия."""
        if self.action == "list":
            return NoteDetailSerializer
        return NoteSerializer

    def get_queryset(self):
        """Получаем заметки на кандидата."""
        candidate = get_object_or_404(Candidate, id=self.kwargs.get("candidate_id"))
        return candidate.user_notes.all()

    def perform_create(self, serializer):
        """Переопределение метода create для записи информация о заметке."""
        candidate = get_object_or_404(Candidate, id=self.kwargs.get("candidate_id"))
        serializer.save(author=self.request.user, candidate=candidate)

    def perform_update(self, serializer):
        """Переопределение метода update для записи информация о заметке."""
        candidate = get_object_or_404(Candidate, id=self.kwargs.get("candidate_id"))
        serializer.save(author=self.request.user, candidate=candidate)


@extend_schema(tags=["Заметки"])
@extend_schema_view(
    list=extend_schema(
        summary="Получить список комментариев к заметке",
        description="Возвращает список всех комментариев к заметке.",
    ),
    create=extend_schema(
        summary="Добавить новый комментарий к заметке",
        description="Добавляет новый комментарий к заметке и сохраняет его в БД.",
    ),
    retrieve=extend_schema(
        summary="Получить детали комментария",
        description="Возвращает детальную информацию о выбранном комментарии.",
    ),
    update=extend_schema(
        summary="Обновить существующий комментарий",
        description="Обновляет данные существующего комментария.",
    ),
    partial_update=extend_schema(
        summary="Частично обновить существующий комментарий",
        description="Обновляет одно или несколько полей существующего комментария.",
    ),
    destroy=extend_schema(
        summary="Удалить комментарий",
        description="Удаляет выбранный комментарий из базы данных.",
    ),
)
class CommentViewSet(ModelViewSet):
    """
    Вьюсет для модели комментариев к заметкам.

    Разрешения:
    IsAuthenticated -- доступ разрешен только аутентифицированным пользователям.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = CommentSerializer
    ordering = ("pub_date",)

    def get_queryset(self):
        """Получаем комментарии к заметке."""
        note = get_object_or_404(Note, id=self.kwargs.get("note_id"))
        return note.comments.all()

    def perform_create(self, serializer):
        """Переопределение метода create для записи информация о комментарии."""
        note = get_object_or_404(Note, id=self.kwargs.get("note_id"))
        serializer.save(author=self.request.user, note=note)

    def perform_update(self, serializer):
        """Переопределение метода update для записи информация о комментарии."""
        note = get_object_or_404(Note, id=self.kwargs.get("note_id"))
        serializer.save(author=self.request.user, note=note)


@extend_schema(tags=["Кандидаты"])
@extend_schema_view(
    list=extend_schema(
        summary="Получить список кандидатов",
        description="Возвращает список всех кандидатов на вакансию.",
    ),
    create=extend_schema(
        summary="Добавить нового кандидата",
        description="Добавляет нового кандидата на вакансию и сохраняет его в БД.",
    ),
    retrieve=extend_schema(
        summary="Получить детали кандидата",
        description="Возвращает детальную информацию о выбранном кандидате.",
    ),
    update=extend_schema(
        summary="Обновить существующего кандидата",
        description="Обновляет данные существующего кандидата.",
    ),
    partial_update=extend_schema(
        summary="Частично обновить существующего кандидата",
        description="Обновляет одно или несколько полей существующего кандидата.",
    ),
    destroy=extend_schema(
        summary="Удалить кандидата",
        description="Удаляет выбранного кандидата из базы данных.",
    ),
)
class CandidateViewSet(ModelViewSet):
    """
    Вьюсет для модели Candidate.

    Разрешения:
    IsAuthenticated -- доступ разрешен только аутентифицированным пользователям.
    """

    permission_classes = (IsAuthenticated,)
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )
    filterset_class = CandidatesFilterSet
    search_fields = (
        "first_name",
        "last_name",
        "city",
        "candidate_status",
        "last_job",
        "cur_position",
        "phone_number",
        "email",
        "telegram",
        "employment_type",
        "schedule_work",
        "education",
        "interview_status",
    )
    ordering_fields = (
        "last_name",
        "city",
        "candidate_status",
        "last_job",
        "cur_position",
        "salary_expectations",
        "vacancy",
        "employment_type",
        "schedule_work",
        "work_experiences",
        "education",
        "interview_status",
        "pub_date",
    )
    ordering = ("pub_date",)

    def get_queryset(self):
        """Получаем кандидатов на вакансию."""
        vacancy = get_object_or_404(Vacancy, pk=self.kwargs.get("vacancy_id"))
        return vacancy.candidates.all()

    def get_serializer_class(self):
        """Функция определяющая сериализатор в зависимости от действия."""
        if self.action == "list":
            return CandidatesSerializer
        return CandidateSerializer

    def perform_create(self, serializer):
        """Переопределение метода create для записи информация о кандидате."""
        vacancy = get_object_or_404(Vacancy, pk=self.kwargs.get("vacancy_id"))
        serializer.save(vacancy=vacancy)

    def perform_update(self, serializer):
        """Переопределение метода update для записи информация о кандидате."""
        vacancy = get_object_or_404(Vacancy, pk=self.kwargs.get("vacancy_id"))
        serializer.save(vacancy=vacancy)


@extend_schema(tags=["Компании"])
@extend_schema_view(
    list=extend_schema(
        summary="Получить список компаний",
        description="Возвращает список всех компаний, доступных текущему пользователю.",
    ),
    create=extend_schema(
        summary="Создать новую компанию",
        description="Создает новую компанию и сохраняет ее в базу данных.",
    ),
    retrieve=extend_schema(
        summary="Получить детали компании",
        description="Возвращает детальную информацию о выбранной компании.",
    ),
    update=extend_schema(
        summary="Обновить существующую компанию",
        description="Обновляет данные существующей компании.",
    ),
    partial_update=extend_schema(
        summary="Частично обновить компанию",
        description="Обновляет одно или несколько полей существующей компании.",
    ),
    destroy=extend_schema(
        summary="Удалить компанию",
        description="Удаляет выбранную компанию из базы данных.",
    ),
)
class CompanyViewSet(ModelViewSet):
    """
    Вьюсет для модели Company.

    Разрешения:
    IsAuthenticated -- доступ разрешен только аутентифицированным пользователям.
    """

    permission_classes = (IsAuthenticated,)
    queryset = Company.objects.all()
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )
    filterset_fields = ("company_address",)
    search_fields = (
        "company_title",
        "company_address",
    )
    ordering_fields = (
        "company_title",
        "company_address",
    )
    ordering = ("company_title",)

    def get_serializer_class(self):
        """Функция определяющая сериализатор в зависимости от действия."""
        if self.action == "list":
            return CompanyShortSerializer
        return CompanySerializer


@extend_schema(tags=["Воронки кандидатов"])
@extend_schema_view(
    list=extend_schema(
        summary="Получить список этапов воронки",
        description="Возвращает список всех этапов воронки кандидата.",
    ),
    create=extend_schema(
        summary="Добавить новый этап в воронку",
        description="Добавляет новый этап в воронку кандидата и сохраняет его в БД.",
    ),
    retrieve=extend_schema(
        summary="Получить детали этапа воронки",
        description="Возвращает детальную информацию о выбранном этапе воронки.",
    ),
    update=extend_schema(
        summary="Обновить существующий этап в воронке",
        description="Обновляет данные существующего этапа в воронке.",
    ),
    partial_update=extend_schema(
        summary="Частично обновить существующий этап в воронке",
        description="Обновляет одно или несколько полей существующего этапа в воронке.",
    ),
    destroy=extend_schema(
        summary="Удалить этап из воронки",
        description="Удаляет выбранный этап из воронки кандидата.",
    ),
)
class FunnelViewSet(ModelViewSet):
    """
    Вьюсет для воронки кандидата Funnel.

    Разрешения:
    IsAuthenticated -- доступ разрешен только аутентифицированным пользователям.
    """

    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        """Функция определяющая сериализатор в зависимости от действия."""
        if self.action == "list" or self.action == "create":
            return FunnelDetailSerializer
        return FunnelSerializer

    def get_queryset(self):
        """Получаем воронку кандидата."""
        candidate = get_object_or_404(Candidate, pk=self.kwargs.get("candidate_id"))
        return candidate.funnel.all()

    def perform_create(self, serializer):
        """Переопределение метода create для записи информация о кандидате."""
        candidate = get_object_or_404(Candidate, pk=self.kwargs.get("candidate_id"))
        serializer.save(candidate=candidate)

    def perform_update(self, serializer):
        """Переопределение метода update для записи информация о кандидате."""
        candidate = get_object_or_404(Candidate, pk=self.kwargs.get("candidate_id"))
        serializer.save(candidate=candidate)


@extend_schema(tags=["Воронки кандидатов"])
@extend_schema_view(
    list=extend_schema(
        summary="Получить список подэтапов",
        description="Возвращает список всех подэтапов воронки кандидата.",
    ),
    create=extend_schema(
        summary="Добавить новый подэтап в воронку",
        description="Добавляет новый подэтап в воронку кандидата и сохраняет его в БД.",
    ),
    retrieve=extend_schema(
        summary="Получить детали подэтапа",
        description="Возвращает детальную информацию о выбранном подэтапе воронки.",
    ),
    update=extend_schema(
        summary="Обновить существующий подэтап в воронке",
        description="Обновляет данные существующего подэтапа в воронке.",
    ),
    partial_update=extend_schema(
        summary="Частично обновить существующий подэтап в воронке",
        description="Обновляет одно или несколько полей подэтапа в воронке.",
    ),
    destroy=extend_schema(
        summary="Удалить подэтап из воронки",
        description="Удаляет выбранный подэтап из воронки кандидата.",
    ),
)
class SubStageViewSet(ModelViewSet):
    """
    Вьюсет для подэтапов воронки кандидата SubStage.

    Разрешения:
    IsAuthenticated -- доступ разрешен только аутентифицированным пользователям.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = SubStageSerializer

    def get_queryset(self):
        """Получаем подэтапы кандидата."""
        funnel = get_object_or_404(FunnelStage, pk=self.kwargs.get("funnel_id"))
        return funnel.substage.all()

    def perform_create(self, serializer):
        """Переопределение метода create для записи информация о воронке."""
        funnel = get_object_or_404(FunnelStage, pk=self.kwargs.get("funnel_id"))
        serializer.save(stage=funnel)

    def perform_update(self, serializer):
        """Переопределение метода update для записи информация о воронке."""
        funnel = get_object_or_404(FunnelStage, pk=self.kwargs.get("funnel_id"))
        serializer.save(stage=funnel)


@extend_schema(tags=["Образование"])
@extend_schema_view(
    list=extend_schema(
        summary="Получить список образовательных учреждений",
        description="Возвращает список всех образовательных учреждений.",
    ),
    create=extend_schema(
        summary="Добавить новое образовательное учреждение",
        description="Добавляет новое образовательное учреждение и сохраняет его в БД.",
    ),
    retrieve=extend_schema(
        summary="Получить детали образовательного учреждения",
        description="Возвращает детальную информацию о выбранном учреждении.",
    ),
    update=extend_schema(
        summary="Обновить существующее образовательное учреждение",
        description="Обновляет данные существующего образовательного учреждения.",
    ),
    partial_update=extend_schema(
        summary="Частично обновить существующее образовательное учреждение",
        description="Обновляет одно или несколько полей образовательного учреждения.",
    ),
    destroy=extend_schema(
        summary="Удалить образовательное учреждение",
        description="Удаляет выбранное образовательное учреждение из базы данных.",
    ),
)
class EducationViewSet(ModelViewSet):
    """
    Вьюсет для модели Education.

    Разрешения:
    IsAuthenticated -- доступ разрешен только аутентифицированным пользователям.
    """

    serializer_class = EducationSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Education.objects.all()
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )
    filterset_fields = (
        "specialization",
        "graduation",
        "educational_institution",
    )
    search_fields = (
        "specialization",
        "graduation",
        "educational_institution",
    )
    ordering_fields = (
        "specialization",
        "graduation",
        "educational_institution",
    )
    ordering = ("specialization",)
