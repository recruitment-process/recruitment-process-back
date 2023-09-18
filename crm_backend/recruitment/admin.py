from django.contrib import admin

from .models import (
    ApplicantResume,
    Candidate,
    Comment,
    Company,
    Education,
    Event,
    FunnelStage,
    Note,
    Skills,
    SkillStack,
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
        "employment_type",
        "schedule_work",
        "working_trip",
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
        "skill_stack",
        "vacancy_status",
        "deadline",
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
        "phone_number",
        "link_hr",
        "website",
    )
    list_filter = ("company_title",)
    search_fields = ("company_title", "email", "phone_number", "link_hr", "website")


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
        # "hr",
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


@admin.register(Skills)
class SkillsAdmin(admin.ModelAdmin):
    """Добавление модели Skills в админку."""

    list_display = ("name",)


@admin.register(SkillStack)
class SkillStackAdmin(admin.ModelAdmin):
    """Добавление модели SkillStack в админку."""

    list_display = (
        "skill_stack",
        "skill_stack_time",
    )


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    """Добавление модели Candidate в админку."""

    list_display = (
        "first_name",
        "last_name",
        "patronymic",
        "bday",
        "city",
        "last_job",
        "cur_position",
        "salary_expectations",
        "phone_number",
        "email",
        "portfolio",
        "resume",
        "photo",
        "employment_type",
        "schedule_work",
        "work_experiences",
        "education",
        "interview_status",
        "custom_status",
        "pub_date",
    )
    list_filter = (
        "cur_position",
        "education",
        "employment_type",
        "schedule_work",
        "salary_expectations",
        "work_experiences",
        "city",
        "interview_status",
        "custom_status",
        "pub_date",
    )
    search_fields = (
        "cur_position",
        "education",
        "salary_expectations",
        "city",
        "employment_type",
        "schedule_work",
        "work_experiences",
        "interview_status",
        "custom_status",
    )
    readonly_fields = ("pub_date",)
    empty_value_display = "-пусто-"


class Comment(admin.TabularInline):
    """Добавление InLine модели Comment в админку."""

    model = Comment


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    """Добавление модели Note в админку."""

    inlines = [
        Comment,
    ]
    list_display = (
        "candidate",
        "text",
        "author",
        "pub_date",
    )
    list_filter = ("candidate", "author", "pub_date")
    search_fields = ("candidate", "author", "pub_date")
    readonly_fields = ("pub_date",)
