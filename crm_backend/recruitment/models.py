from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from multiselectfield import MultiSelectField
from recruitment.constants_choices_resume import (
    EDUCATION,
    EMPLOYMENT_TYPE,
    GENDER,
    MARITAL_STATUS,
    RELOCATION,
    SCHEDULE_WORK,
)
from users.models import User


class Work_Experience(models.Model):
    """Опыт работы."""

    start_date = models.DateField(verbose_name="Дата устроения")
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
        # Проверяем, что end_date не меньше start_date
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError(
                "Дата увольнения не может быть меньше даты устройства."
            )


class Applicant_Resume(models.Model):
    """Резюме"""

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
    phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    phoneNumber = models.CharField(
        validators=[phoneNumberRegex],
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
        Work_Experience,
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
        Applicant_Resume,
        on_delete=models.CASCADE,
        related_name="educations",
        verbose_name="резюме",
    )

    class Meta:
        ordering = ["graduation"]
        verbose_name = "Информация об образовавании"

    def __str__(self):
        return self.specialization
