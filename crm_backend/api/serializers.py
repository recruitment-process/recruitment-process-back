from datetime import date

from recruitment.constants import (
    EDUCATION,
    EMPLOYMENT_TYPE,
    GENDER,
    INTERVIEW_STATUS,
    RELOCATION,
    SCHEDULE_WORK,
    VACANCY_STATUS,
)
from recruitment.models import ApplicantResume, Vacancy
from rest_framework.serializers import (
    ChoiceField,
    ModelSerializer,
    SerializerMethodField,
    StringRelatedField,
    ValidationError,
)

from .constants import MAX_AGE, MIN_AGE
from .utils import DateOnlyField, get_display_values


class VacancySerializer(ModelSerializer):
    """Сериализатор карточки вакансии."""

    company = StringRelatedField(read_only=True)
    author = StringRelatedField(read_only=True)
    schedule_work = SerializerMethodField()
    employment_type = SerializerMethodField()
    status = SerializerMethodField()
    pub_date = DateOnlyField()

    class Meta:
        model = Vacancy
        fields = (
            "vacancy_title",
            "company",
            "required_experience",
            "employment_type",
            "schedule_work",
            "salary",
            "about_company",
            "city",
            "address",
            "pub_date",
            "job_conditions",
            "job_responsibilities",
            "technology_stack",
            "status",
            "author",
            "deadline",
        )
        read_only_fields = ("author",)

    def get_schedule_work(self, obj):
        """
        Функция преобразования вывода информации.

        Для поля schedule_work с ключа на значение.
        """
        return get_display_values(obj.schedule_work, SCHEDULE_WORK)

    def get_employment_type(self, obj):
        """
        Функция преобразования вывода информации.

        Для поля employment_type с ключа на значение.
        """
        return get_display_values(obj.employment_type, EMPLOYMENT_TYPE)

    def get_status(self, obj):
        """
        Функция преобразования вывода информации.

        Для поля status с ключа на значение.
        """
        return get_display_values(obj.status, VACANCY_STATUS)


class VacanciesSerializer(ModelSerializer):
    """Сериализатор для просмотра карточек вакансий."""

    company = StringRelatedField(read_only=True)
    schedule_work = SerializerMethodField()
    employment_type = SerializerMethodField()

    class Meta:
        model = Vacancy
        fields = (
            "vacancy_title",
            "company",
            "required_experience",
            "employment_type",
            "schedule_work",
            "salary",
            "city",
            "technology_stack",
            "deadline",
        )

    def get_schedule_work(self, obj):
        """
        Функция преобразования вывода информации.

        Для поля schedule_work с ключа на значение.
        """
        return get_display_values(obj.schedule_work, SCHEDULE_WORK)

    def get_employment_type(self, obj):
        """
        Функция преобразования вывода информации.

        Для поля employment_type с ключа на значение.
        """
        return get_display_values(obj.employment_type, EMPLOYMENT_TYPE)


class ResumeSerializer(ModelSerializer):
    """Сериализатор карточки резюме."""

    schedule_work = SerializerMethodField()
    employment_type = SerializerMethodField()
    gender = SerializerMethodField()
    relocation = ChoiceField(choices=RELOCATION)
    education = ChoiceField(choices=EDUCATION)
    age = SerializerMethodField()
    interview_status = ChoiceField(choices=INTERVIEW_STATUS)

    class Meta:
        model = ApplicantResume
        fields = (
            "applicant",
            "job_title",
            "employment_type",
            "schedule_work",
            "salary",
            "working_trip",
            "phone_number",
            "relocation",
            "pub_date",
            "gender",
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

        Для поля schedule_work с ключа на значение.
        """
        return get_display_values(obj.schedule_work, SCHEDULE_WORK)

    def get_employment_type(self, obj):
        """
        Функция преобразования вывода информации.

        Для поля employment_type с ключа на значение.
        """
        return get_display_values(obj.employment_type, EMPLOYMENT_TYPE)

    def get_gender(self, obj):
        """
        Функция преобразования вывода информации.

        Для поля gender с ключа на значение.
        """
        return get_display_values(obj.gender, GENDER)

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


class ResumesSerializer(ModelSerializer):
    """Сериализатор для карточек резюме."""

    class Meta:
        model = ApplicantResume
        fields = (
            "applicant",
            "job_title",
            "salary",
            "work_experiences",
            "current_company",
            "interview_status",
        )
