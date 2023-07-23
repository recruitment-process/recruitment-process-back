from django.contrib import admin

from .models import Applicant_Resume, Education, Work_Experience


@admin.register(Applicant_Resume)
class Applicant_ResumeAdmin(admin.ModelAdmin):
    pass


@admin.register(Work_Experience)
class Work_Experience(admin.ModelAdmin):
    pass


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    pass
