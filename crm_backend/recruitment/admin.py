from django.conf import settings
from django.contrib import admin

from .models import Applicant_resume, Work_experience, Education


@admin.register(Applicant_resume)
class Applicant_resumeAdmin(admin.ModelAdmin):
    pass


@admin.register(Work_experience)
class Work_experience(admin.ModelAdmin):
    pass


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    pass
