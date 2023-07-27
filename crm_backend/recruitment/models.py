from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from multiselectfield import MultiSelectField
from recruitment.constants import (
    EDUCATION,
    EMPLOYMENT_TYPE,
    EXPERIENCE,
    GENDER,
    MARITAL_STATUS,
    RELOCATION,
    SCHEDULE_WORK,
)

User = get_user_model()


class WorkExperience(models.Model):
    """Модель опыта работы."""

    start_date = models.DateField(verbose_name="Дата начала работы")
    end_date = models.DateField(
        verbose_name="Дата увольнения",
        null=True,
        blank=True,
    )
    position = models.CharField(
        max_length=50,
        verbose_name="Должность",
    )
    organization = models.CharField(
        max_length=50,
        verbose_name="Организация",
    )

    class Meta:
        verbose_name = "Опыт работы"

    def __str__(self):
        return f"{self.position} - {self.organization}"

    def clean(self):
        """Функция для проверки корректности end_date и start_date."""
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError(
                "Дата увольнения не может быть меньше даты устройства на работу!"
            )


class ApplicantResume(models.Model):
    """Модель резюме."""

    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="applicant_resumes",
        verbose_name="Соискатель",
    )
    job_title = models.CharField(
        max_length=100,
        verbose_name="Должность",
    )

    employment_type = MultiSelectField(
        choices=EMPLOYMENT_TYPE,
        verbose_name="Тип занятости",
    )
    schedule_work = MultiSelectField(
        choices=SCHEDULE_WORK,
        verbose_name="Расписание работы",
    )

    salary = models.CharField(
        max_length=50,
        verbose_name="Желаемая зарплата",
    )
    working_trip = models.BooleanField(
        null=True,
        blank=True,
        verbose_name="Командировка",
    )
    phone_number_regex = RegexValidator(regex=r"^\+?1?\d{10,15}$")
    phone_number = models.CharField(
        validators=[phone_number_regex],
        max_length=16,
    )
    relocation = models.CharField(
        max_length=2,
        choices=RELOCATION,
        verbose_name="Переезд",
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER,
        verbose_name="Пол",
    )
    marital_status = models.CharField(
        max_length=1,
        choices=MARITAL_STATUS,
        verbose_name="Семейное положение",
    )
    education = models.CharField(
        max_length=2,
        choices=EDUCATION,
        verbose_name="Образование",
    )
    town = models.CharField(
        max_length=50,
        verbose_name="Город проживания",
    )
    citizenship = models.CharField(
        max_length=50,
        verbose_name="Гражданство",
    )
    bday = models.DateField(
        auto_now=False,
        auto_now_add=False,
        verbose_name="Дата рождения",
    )
    work_experiences = models.ManyToManyField(
        WorkExperience,
        verbose_name="Информация об опыте работы",
    )
    about_me = models.TextField(
        max_length=700,
        verbose_name="Коротко о себе",
    )

    class Meta:
        ordering = ["job_title"]
        verbose_name = "Резюме"

    def __str__(self):
        return f"{self.applicant} - {self.job_title}"


class Education(models.Model):
    """Информация об образовании."""

    educational_institution = models.CharField(
        max_length=250,
        verbose_name="Учебное заведение",
    )
    faculty = models.CharField(
        max_length=100,
        verbose_name="Факультет",
    )
    specialization = models.CharField(
        max_length=100,
        verbose_name="Специальность",
    )
    graduation = models.DateField(
        verbose_name="Год окончания",
        null=True,
        blank=True,
    )
    resume = models.ForeignKey(
        ApplicantResume,
        on_delete=models.CASCADE,
        related_name="educations",
        verbose_name="резюме",
    )

    class Meta:
        ordering = ["graduation"]
        verbose_name = "Информация об образовавании"

    def __str__(self):
        return self.specialization


class Company(models.Model):
    """Информация о компании."""

    company_title = models.CharField(
        max_length=100,
        verbose_name="Название компании",
    )
    about_company = models.TextField(
        verbose_name="О компании",
        help_text="Введите информацию о компани",
    )

    company_address = models.CharField(
        max_length=100,
        verbose_name="Адрес компании",
    )

    email = models.EmailField(
        verbose_name="Эл.почта",
    )

    phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{10,15}$")

    phoneNumber = models.CharField(
        validators=[phoneNumberRegex],
        max_length=16,
        null=True,
    )

    link_hr = models.URLField(
        max_length=100,
        verbose_name="Ссылка на HR",
        null=True,
    )

    class Meta:
        ordering = ["company_title"]
        verbose_name = "Основная информация о компании"

    def __str__(self):
        return self.company_title


class Vacancy(models.Model):
    """Модель Вакансий."""

    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Компания",
        related_name="vacancies",
    )

    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Автор",
        related_name="vacancies",
    )

    vacancy_title = models.CharField(
        max_length=100,
        verbose_name="Название вакансии",
    )

    required_experience = models.CharField(
        max_length=1,
        choices=EXPERIENCE,
        verbose_name="Требуемый опыт работы",
        blank=False,
    )

    employment_type = MultiSelectField(
        choices=EMPLOYMENT_TYPE,
        verbose_name="Тип занятости",
        blank=False,
        default=["PO"],
    )

    schedule_work = MultiSelectField(
        choices=SCHEDULE_WORK,
        verbose_name="Расписание работы",
        blank=False,
        default=["P"],
    )

    about_company = models.TextField(
        verbose_name="О компании",
        help_text="Введите информацию о компани",
    )

    pub_date = models.DateTimeField(
        "Дата публикации вакансии",
        auto_now_add=True,
    )

    job_conditions = models.TextField(
        verbose_name="Условия работы",
        help_text="Введите условия работы",
    )

    job_responsibilities = models.TextField(
        verbose_name="Обязанности кандидата",
        help_text="Введите обязанности кандидата",
    )

    technology_stack = (
        # позже можно будет сделать бд со всеми навыками
        models.TextField(
            verbose_name="Ключевые навыки",
        )
    )

    class Meta:
        ordering = ["pub_date"]
        verbose_name = "Основная информация о вакансии"

    def __str__(self):
        return self.vacancy_title
