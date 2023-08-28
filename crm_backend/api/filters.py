from django_filters import BooleanFilter, ChoiceFilter, FilterSet, filters
from recruitment.constants import (
    EDUCATION,
    EMPLOYMENT_TYPE,
    EXPERIENCE,
    INTERVIEW_STATUS,
    RELOCATION,
    SCHEDULE_WORK,
    VACANCY_STATUS,
)
from recruitment.models import ApplicantResume, Vacancy


class VacancyFilterSet(FilterSet):
    """Кастомный фильтр для зарплат."""

    salary = filters.BaseCSVFilter(field_name="salary", lookup_expr="contains")
    employment_type = ChoiceFilter(
        field_name="employment_type", choices=EMPLOYMENT_TYPE
    )
    schedule_work = ChoiceFilter(field_name="schedule_work", choices=SCHEDULE_WORK)
    vacancy_status = ChoiceFilter(field_name="vacancy_status", choices=VACANCY_STATUS)
    required_experience = ChoiceFilter(
        field_name="required_experience", choices=EXPERIENCE
    )

    class Meta:
        model = Vacancy
        fields = [
            "salary",
            "vacancy_title",
            "author",
            "company",
            "required_experience",
            "employment_type",
            "schedule_work",
            "city",
            "pub_date",
            "vacancy_status",
            "technology_stack",
            "deadline",
        ]


class ResumeFilterSet(FilterSet):
    """Кастомный фильтр для зарплат."""

    salary_expectations = filters.BaseCSVFilter(
        field_name="salary_expectations", lookup_expr="contains"
    )
    employment_type = ChoiceFilter(
        field_name="employment_type", choices=EMPLOYMENT_TYPE
    )
    schedule_work = ChoiceFilter(field_name="schedule_work", choices=SCHEDULE_WORK)
    education = ChoiceFilter(field_name="education", choices=EDUCATION)
    relocation = ChoiceFilter(field_name="relocation", choices=RELOCATION)
    work_experiences = ChoiceFilter(field_name="work_experiences", choices=EXPERIENCE)
    interview_status = ChoiceFilter(
        field_name="interview_status", choices=INTERVIEW_STATUS
    )
    working_trip = BooleanFilter(field_name="working_trip")

    class Meta:
        model = ApplicantResume
        fields = [
            "salary_expectations",
            "job_title",
            "employment_type",
            "schedule_work",
            "working_trip",
            "relocation",
            "pub_date",
            "education",
            "town",
            "citizenship",
            "bday",
            "work_experiences",
            "interview_status",
        ]
