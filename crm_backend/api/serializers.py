import re
from datetime import date

from recruitment.constants import (
    EDUCATION,
    EMPLOYMENT_TYPE,
    INTERVIEW_STATUS,
    RELOCATION,
    SCHEDULE_WORK,
    VACANCY_STATUS,
)
from recruitment.models import ApplicantResume, Company, Vacancy, WorkExperience
from rest_framework.serializers import (
    CharField,
    ChoiceField,
    EmailField,
    ModelSerializer,
    SerializerMethodField,
    StringRelatedField,
    ValidationError,
)
from users.models import User
from users.validators import custom_validate_email

from .constants import MAX_AGE, MIN_AGE
from .utils import (
    DateOnlyField,
    get_display_values,
    get_salary_expectations,
    get_salary_range,
)


class UserSignupSerializer(ModelSerializer):
    """Сериализатор пользователя при регистрации."""

    password = CharField(max_length=255)
    email = EmailField(max_length=255)

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
            raise ValidationError("Минимальная длина пароля 8 символов!")
        if not re.match(r"^[^\sа-яА-Я]+$", value):
            raise ValidationError(
                "Пароль не должен содержать невидимые символы и кириллицу!"
            )
        return value

    def validate(self, data):
        """Проверка на существование пользователя с email."""
        email = data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError(f"Пользователь с адресом {email} уже существует")
        return data


class CompanySerializer(ModelSerializer):
    """Сериализатор для модели Company."""

    class Meta:
        model = Company
        fields = "__all__"


class WorkExperienceSerializer(ModelSerializer):
    """Сериализатор карточки опыта работы."""

    experience_length = SerializerMethodField()

    class Meta:
        model = WorkExperience
        fields = (
            "start_date",
            "end_date",
            "position",
            "organization",
            "experience_length",
        )

    def get_experience_length(self, obj):
        """
        Функция для вычисления продолжительности работы.

        Возвращает количество месяцев и лет работы.
        """
        today = date.today()
        if obj.end_date:
            experience_length = (today - obj.start_date).days / 30
            years = experience_length // 12
            months = experience_length % 12
            return f"{int(years)} года/лет и {round(months)} месяца(ев)"


class VacancySerializer(ModelSerializer):
    """Сериализатор карточки вакансии."""

    company = CompanySerializer(read_only=True)
    author = StringRelatedField(read_only=True)
    schedule_work = SerializerMethodField()
    employment_type = SerializerMethodField()
    vacancy_status = SerializerMethodField()
    pub_date = DateOnlyField()
    salary_range = SerializerMethodField()

    class Meta:
        model = Vacancy
        fields = (
            "vacancy_title",
            "company",
            "required_experience",
            "employment_type",
            "schedule_work",
            "salary_range",
            "about_company",
            "city",
            "address",
            "pub_date",
            "job_conditions",
            "job_responsibilities",
            "technology_stack",
            "vacancy_status",
            "author",
            "deadline",
        )
        read_only_fields = ("author",)

    def get_schedule_work(self, obj):
        """
        Функция преобразования вывода информации.

        Возвращает значение поля schedule_work.
        """
        return get_display_values(obj.schedule_work, SCHEDULE_WORK)

    def get_employment_type(self, obj):
        """
        Функция преобразования вывода информации.

        Возвращает значение поля employment_type.
        """
        return get_display_values(obj.employment_type, EMPLOYMENT_TYPE)

    def get_vacancy_status(self, obj):
        """
        Функция преобразования вывода информации.

        Возвращает значение поля vacancy_status.
        """
        return get_display_values(obj.vacancy_status, VACANCY_STATUS)

    def get_salary_range(self, obj):
        """Функция преобразования вывода информации для поля salary."""
        return get_salary_range(obj)


class VacanciesSerializer(ModelSerializer):
    """Сериализатор для просмотра карточек вакансий."""

    company = StringRelatedField(read_only=True)
    schedule_work = SerializerMethodField()
    employment_type = SerializerMethodField()
    salary_range = SerializerMethodField()

    class Meta:
        model = Vacancy
        fields = (
            "vacancy_title",
            "company",
            "required_experience",
            "employment_type",
            "schedule_work",
            "salary_range",
            "city",
            "technology_stack",
            "deadline",
        )

    def get_schedule_work(self, obj):
        """
        Функция преобразования вывода информации.

        Возвращает значение поля schedule_work.
        """
        return get_display_values(obj.schedule_work, SCHEDULE_WORK)

    def get_employment_type(self, obj):
        """
        Функция преобразования вывода информации.

        Возвращает значение поля employment_type.
        """
        return get_display_values(obj.employment_type, EMPLOYMENT_TYPE)

    def get_salary_range(self, obj):
        """Функция преобразования вывода информации для поля salary."""
        return get_salary_range(obj)


class ResumeSerializer(ModelSerializer):
    """Сериализатор карточки резюме."""

    schedule_work = SerializerMethodField()
    employment_type = SerializerMethodField()
    relocation = ChoiceField(choices=RELOCATION)
    education = ChoiceField(choices=EDUCATION)
    age = SerializerMethodField()
    interview_status = ChoiceField(choices=INTERVIEW_STATUS)
    salary_expectations = SerializerMethodField()
    work_experiences = WorkExperienceSerializer(many=True)

    class Meta:
        model = ApplicantResume
        fields = (
            "applicant",
            "job_title",
            "employment_type",
            "schedule_work",
            "salary_expectations",
            "working_trip",
            "phone_number",
            "relocation",
            "pub_date",
            "education",
            "town",
            "citizenship",
            "bday",
            "age",
            "work_experiences",
            "about_me",
            "current_company",
            "current_job",
            "interview_status",
        )

    def get_schedule_work(self, obj):
        """
        Функция преобразования вывода информации.

        Возвращает значение поля schedule_work.
        """
        return get_display_values(obj.schedule_work, SCHEDULE_WORK)

    def get_employment_type(self, obj):
        """
        Функция преобразования вывода информации.

        Возвращает значение поля employment_type.
        """
        return get_display_values(obj.employment_type, EMPLOYMENT_TYPE)

    def get_age(self, obj):
        """Функция для подсчета возраста соискателя."""
        today = date.today()
        born = obj.bday
        return (
            today.year - born.year - ((today.month, today.day) < (born.month, born.day))
        )

    def validate_bday(self, obj):
        """Функция валидации даты рождения соискателя."""
        today = date.today()
        born = obj.bday
        if not (MAX_AGE > (today.year - born.year) > MIN_AGE):
            raise ValidationError("Проверьте дату рождения!")
        return obj

    def get_salary_expectations(self, obj):
        """Функция преобразования вывода информации для поля salary_expectations."""
        return get_salary_expectations(obj)


class ResumesSerializer(ModelSerializer):
    """Сериализатор для карточек резюме."""

    class Meta:
        model = ApplicantResume
        fields = (
            "applicant",
            "job_title",
            "work_experiences",
            "current_company",
            "interview_status",
        )
