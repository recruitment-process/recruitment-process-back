from datetime import date

from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, validate_email
from django.db import models
from multiselectfield import MultiSelectField
from multiselectfield.utils import get_max_length
from recruitment.constants import (
    DEADLINE,
    EDUCATION,
    EMPLOYMENT_TYPE,
    EXPERIENCE,
    FUNNEL_STATUS,
    INTERVIEW_STATUS,
    PHONE_NUMBER_REGEX,
    SCHEDULE_WORK,
    VACANCY_STATUS,
    VALID_TELEGRAM_REGEX,
)
from users.models import User
from users.validators import custom_validate_email

from .utils import generate_logo_path, upload_to_candidates


class WorkExperience(models.Model):
    """Модель опыта работы."""

    start_date = models.DateField(verbose_name="Дата начала работы")
    end_date = models.DateField(
        verbose_name="Дата увольнения",
        default=date.today(),
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
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Опыт работы"
        verbose_name_plural = "Опыт работы"

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
        null=True,
        blank=True,
        max_length=get_max_length(EMPLOYMENT_TYPE, None),
    )
    schedule_work = MultiSelectField(
        choices=SCHEDULE_WORK,
        verbose_name="Расписание работы",
        null=True,
        blank=True,
        max_length=get_max_length(SCHEDULE_WORK, None),
    )
    salary_expectations = ArrayField(
        models.IntegerField(),
        size=2,
        null=True,
        blank=True,
        verbose_name="Желаемая зарплата",
    )
    working_trip = models.BooleanField(
        null=True,
        blank=True,
        verbose_name="Командировка",
    )
    phone_number = models.CharField(
        validators=[PHONE_NUMBER_REGEX],
        max_length=16,
    )
    education = models.CharField(
        max_length=2,
        choices=EDUCATION,
        verbose_name="Образование",
        null=True,
        blank=True,
    )
    town = models.CharField(
        max_length=40,
        verbose_name="Город проживания",
        null=True,
        blank=True,
    )
    citizenship = models.CharField(
        max_length=40,
        verbose_name="Гражданство",
        null=True,
        blank=True,
    )
    bday = models.DateField(
        auto_now=False,
        auto_now_add=False,
        verbose_name="Дата рождения",
    )
    work_experiences = models.ManyToManyField(
        WorkExperience,
        verbose_name="Информация об опыте работы",
        blank=True,
    )
    about_me = models.TextField(
        max_length=700,
        verbose_name="Коротко о себе",
        blank=True,
        null=True,
    )
    current_company = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Текущее место работы",
    )
    current_job = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Текущяя должность",
    )
    pub_date = models.DateTimeField(
        "Дата публикации резюме",
        auto_now_add=True,
    )

    class Meta:
        ordering = ["job_title"]
        verbose_name = "Резюме"
        verbose_name_plural = "Резюме"

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
        blank=True,
        null=True,
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
        verbose_name_plural = "Информация об образовавании"

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
        null=True,
        blank=True,
    )
    company_address = models.CharField(
        max_length=100,
        verbose_name="Адрес компании",
        null=True,
        blank=True,
    )
    website = models.URLField(
        max_length=255,
        verbose_name="Сайт компании",
    )
    email = models.EmailField(
        verbose_name="Эл.почта",
        null=True,
        blank=True,
    )
    phone_number = models.CharField(
        validators=[PHONE_NUMBER_REGEX],
        max_length=16,
        null=True,
        blank=True,
    )
    link_hr = models.URLField(
        max_length=250,
        verbose_name="Ссылка на HR",
        null=True,
        blank=True,
    )
    logo = models.ImageField(
        upload_to=generate_logo_path,
        verbose_name="Логотип компании",
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["company_title"]
        verbose_name = "Компания"
        verbose_name_plural = "Компании"

    def __str__(self):
        return self.company_title


class Vacancy(models.Model):
    """Модель Вакансий."""

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name="Компания",
        related_name="vacancies",
    )
    # Надо будет переписать на промежуточную таблицу ManyToMany с ссылками на HR'ов
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
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
        null=True,
        blank=True,
    )
    employment_type = MultiSelectField(
        choices=EMPLOYMENT_TYPE,
        verbose_name="Тип занятости",
        null=True,
        blank=True,
        max_length=get_max_length(EMPLOYMENT_TYPE, None),
    )
    schedule_work = MultiSelectField(
        choices=SCHEDULE_WORK,
        verbose_name="Расписание работы",
        null=True,
        blank=True,
        max_length=get_max_length(SCHEDULE_WORK, None),
    )
    salary = ArrayField(
        models.IntegerField(),
        size=2,
        null=True,
        blank=True,
        verbose_name="Оплата труда",
    )
    city = models.CharField(
        max_length=40,
        verbose_name="Город",
    )
    education = models.CharField(
        max_length=5,
        choices=EDUCATION,
        verbose_name="Образование",
        null=True,
        blank=True,
    )
    pub_date = models.DateTimeField(
        "Дата публикации вакансии",
        auto_now_add=True,
    )
    job_conditions = models.TextField(
        verbose_name="Условия работы",
        help_text="Введите условия работы",
        null=True,
        blank=True,
        max_length=1400,
    )
    job_responsibilities = models.TextField(
        verbose_name="Обязанности кандидата",
        help_text="Введите обязанности кандидата",
        null=True,
        blank=True,
        max_length=1400,
    )
    technology_stack = (
        # позже нужно будет сделать бд со всеми навыками
        models.TextField(
            verbose_name="Ключевые навыки",
        )
    )
    vacancy_status = models.CharField(
        max_length=1,
        choices=VACANCY_STATUS,
        verbose_name="Статус вакансии",
        blank=False,
    )
    deadline = models.DateField(default=DEADLINE, verbose_name="Срок закрытия вакансии")

    class Meta:
        ordering = ["pub_date"]
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"

    def __str__(self):
        return self.vacancy_title


class Candidate(models.Model):
    """Модель кандидата."""

    first_name = models.CharField(
        max_length=40,
        verbose_name="Имя",
        validators=[MinLengthValidator(2)],
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name="Фамилия",
        validators=[MinLengthValidator(2)],
    )
    patronymic = models.CharField(
        max_length=50,
        verbose_name="Отчество",
        null=True,
        blank=True,
        validators=[MinLengthValidator(2)],
    )
    bday = models.DateField(
        auto_now=False,
        auto_now_add=False,
        verbose_name="Дата рождения",
    )
    city = models.CharField(
        max_length=40,
        verbose_name="Город проживания",
        validators=[MinLengthValidator(2)],
    )
    last_job = models.CharField(
        max_length=90,
        verbose_name="Последнее место работы",
        null=True,
        blank=True,
        validators=[MinLengthValidator(2)],
    )
    cur_position = models.CharField(
        max_length=50,
        verbose_name="Текущая должность",
        null=True,
        blank=True,
        validators=[MinLengthValidator(2)],
    )
    salary_expectations = ArrayField(
        models.IntegerField(),
        size=2,
        null=True,
        blank=True,
        verbose_name="Желаемая зарплата",
    )
    vacancy = models.ForeignKey(
        Vacancy,
        on_delete=models.CASCADE,
        verbose_name="Вакансия",
        related_name="candidates",
    )
    phone_number = models.CharField(
        validators=[PHONE_NUMBER_REGEX],
        max_length=16,
        verbose_name="Телефон",
        default="89501002030",
    )
    email = models.EmailField(
        verbose_name="Почта",
        max_length=256,
        unique=True,
        validators=[MinLengthValidator(2), validate_email, custom_validate_email],
    )
    telegram = models.CharField(
        max_length=150,
        validators=[VALID_TELEGRAM_REGEX],
        verbose_name="Телеграмм",
        null=True,
        blank=True,
    )
    portfolio = models.URLField(
        max_length=255,
        verbose_name="Ссылка на портфолио",
        null=True,
        blank=True,
    )
    resume = models.FileField(
        verbose_name="Резюме",
        upload_to=upload_to_candidates,
        null=True,
        blank=True,
    )
    photo = models.ImageField(
        upload_to=upload_to_candidates,
        verbose_name="Фотография",
        null=True,
        blank=True,
    )
    employment_type = MultiSelectField(
        choices=EMPLOYMENT_TYPE,
        verbose_name="Тип занятости",
        null=True,
        blank=True,
        max_length=get_max_length(EMPLOYMENT_TYPE, None),
    )
    schedule_work = MultiSelectField(
        choices=SCHEDULE_WORK,
        verbose_name="Расписание работы",
        null=True,
        blank=True,
        max_length=get_max_length(SCHEDULE_WORK, None),
    )
    work_experiences = models.CharField(
        max_length=1,
        choices=EXPERIENCE,
        null=True,
        blank=True,
        verbose_name="Информация об опыте работы",
    )
    education = models.CharField(
        max_length=2,
        choices=EDUCATION,
        verbose_name="Образование",
        null=True,
        blank=True,
    )
    interview_status = models.CharField(
        max_length=5,
        choices=INTERVIEW_STATUS,
        null=True,
        blank=True,
        verbose_name="Статус",
    )
    custom_status = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Собственный статус",
    )
    pub_date = models.DateTimeField(
        "Дата добавления кандидата резюме",
        auto_now_add=True,
    )

    class Meta:
        ordering = ["pub_date"]
        verbose_name = "Кандидат"
        verbose_name_plural = "Кандидаты"

    def __str__(self):
        return self.last_name


class Event(models.Model):
    """Модель создания событий в календаре."""

    title = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(
        blank=True,
        null=True,
    )
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    description = models.TextField(
        blank=True,
        null=True,
    )
    # hr = models.ForeignKey(
    #    settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="events"
    # )
    conference_link = models.URLField(
        max_length=255,
        blank=True,
        null=True,
    )
    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE,
        related_name="candidate_events",
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ["start_date"]
        verbose_name = "Событие"
        verbose_name_plural = "События"

    def __str__(self):
        return self.title


class FunnelStage(models.Model):
    """Этапы воронки."""

    name = models.CharField(max_length=100, verbose_name="Название этапа")
    date = models.DateField(blank=True, null=True, verbose_name="Дата")
    status = models.CharField(
        choices=FUNNEL_STATUS,
        max_length=get_max_length(FUNNEL_STATUS, None),
        default=FUNNEL_STATUS[0][0],
        verbose_name="Статус этапа",
    )
    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE,
        verbose_name="Кандидат",
        related_name="funnel",
    )

    class Meta:
        ordering = ["-date"]
        verbose_name = "Воронка кандидата"
        verbose_name_plural = "Воронки кандидатов"

    def __str__(self):
        return self.name


class SubStage(models.Model):
    """Подэтапы воронки."""

    name = models.CharField(max_length=100, verbose_name="Название подэтапа")
    date = models.DateField(blank=True, null=True, verbose_name="Дата")
    status = models.CharField(
        choices=FUNNEL_STATUS,
        max_length=get_max_length(FUNNEL_STATUS, None),
        default=FUNNEL_STATUS[0][0],
        verbose_name="Статус подэтапа",
    )
    stage = models.ForeignKey(
        FunnelStage,
        on_delete=models.CASCADE,
        verbose_name="Этап воронки",
        related_name="substage",
    )

    class Meta:
        ordering = ["-date"]
        verbose_name = "Подэтап воронки"
        verbose_name_plural = "Подэтапы воронок"

    def __str__(self):
        return self.name


class Note(models.Model):
    """Модель Заметок."""

    candidate = models.ForeignKey(
        Candidate, on_delete=models.CASCADE, verbose_name="Кандидат"
    )
    text = models.TextField("Текст", help_text="Заметка")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_notes"
    )
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)

    class Meta:
        ordering = ("-pub_date",)

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Модель комментария к заметкам."""

    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name="notes")
    text = models.TextField("Текст", help_text="Комментарий")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)

    class Meta:
        ordering = ("-pub_date",)

    def __str__(self):
        return self.text
