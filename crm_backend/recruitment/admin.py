from django.contrib import admin

from .models import ApplicantResume, Company, Education, Vacancy, WorkExperience


@admin.register(ApplicantResume)
class ApplicantResumeAdmin(admin.ModelAdmin):
    """Добавление модели ApplicantResume в админку."""

    pass


@admin.register(WorkExperience)
class WorkExperience(admin.ModelAdmin):
    """Добавление модели WorkExperience в админку."""

    pass


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    """Добавление модели Education в админку."""

    pass


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    """Добавление модели Vacancy в админку."""

    pass


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    """Добавление модели Company в админку."""

    pass
