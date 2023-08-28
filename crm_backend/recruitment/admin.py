from django.contrib import admin

from .models import (
    ApplicantResume,
    Company,
    Education,
    Event,
    FunnelStage,
    SubStage,
    Vacancy,
    WorkExperience,
)


@admin.register(ApplicantResume)
class ApplicantResumeAdmin(admin.ModelAdmin):
    """Добавление модели ApplicantResume в админку."""

    list_display = (
        "job_title",
        "education",
        "bday",
        "salary_expectations",
        "town",
        "citizenship",
    )
    list_filter = ("job_title", "education", "salary_expectations", "town")
    search_fields = (
        "job_title",
        "education",
        "salary_expectations",
        "town",
        "citizenship",
    )
    empty_value_display = "-пусто-"


@admin.register(WorkExperience)
class WorkExperience(admin.ModelAdmin):
    """Добавление модели WorkExperience в админку."""

    list_display = ("position", "organization", "start_date", "end_date")
    list_filter = ("position", "organization", "end_date")
    search_fields = ("position", "organization", "end_date")
    empty_value_display = "-пусто-"


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    """Добавление модели Education в админку."""

    list_display = ("specialization", "educational_institution", "graduation", "resume")
    list_filter = ("specialization", "graduation")
    search_fields = ("specialization", "graduation")
    empty_value_display = "-пусто-"


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    """Добавление модели Vacancy в админку."""

    list_display = (
        "vacancy_title",
        "company",
        "required_experience",
        "employment_type",
        "schedule_work",
    )
    list_filter = ("vacancy_title", "company", "employment_type", "schedule_work")
    search_fields = (
        "vacancy_title",
        "company",
        "employment_type",
        "schedule_work",
    )


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    """Добавление модели Company в админку."""

    list_display = (
        "company_title",
        "company_address",
        "email",
        "website",
        "phone_number",
        "link_hr",
    )
    list_filter = ("company_title",)
    search_fields = ("company_title", "email", "phone_number", "link_hr")


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """Добавление модели Event в админку."""

    list_display = (
        "title",
        "start_date",
        "end_date",
        "start_time",
        "end_time",
        "description",
        "conference_link",
        "hr",
        "candidate",
    )
    list_filter = ("start_date", "end_date", "title", "start_time", "end_time")
    search_fields = (
        "start_date",
        "title",
        "candidate",
        "start_time",
        "end_time",
    )


class SubStage(admin.TabularInline):
    """Добавление InLine модели SubStage в админку."""

    model = SubStage


@admin.register(FunnelStage)
class FunnelStageAdmin(admin.ModelAdmin):
    """Добавление модели FunnelStage в админку."""

    inlines = [
        SubStage,
    ]
    list_display = (
        "candidate",
        "name",
        "date",
        "status",
    )
    list_filter = ("candidate", "name", "date", "status")
    search_fields = ("candidate",)
