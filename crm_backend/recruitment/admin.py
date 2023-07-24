from django.contrib import admin

from .models import ApplicantResume, Education, WorkExperience


@admin.register(ApplicantResume)
class ApplicantResumeAdmin(admin.ModelAdmin):
    pass


@admin.register(WorkExperience)
class WorkExperience(admin.ModelAdmin):
    pass


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    pass
