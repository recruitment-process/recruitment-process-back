from django_filters import (
    BooleanFilter,
    CharFilter,
    ChoiceFilter,
    FilterSet,
    MultipleChoiceFilter,
    filters,
)
from recruitment.constants import (
    CANDIDATE_STATUS,
    EDUCATION,
    EMPLOYMENT_TYPE,
    EXPERIENCE,
    INTERVIEW_STATUS,
    SCHEDULE_WORK,
    VACANCY_STATUS,
)
from recruitment.models import ApplicantResume, Candidate, Vacancy


class VacancyFilterSet(FilterSet):
    """Кастомный фильтр для вакансий."""

    salary = filters.BaseCSVFilter(field_name="salary", lookup_expr="contains")
    employment_type = MultipleChoiceFilter(
        field_name="employment_type", choices=EMPLOYMENT_TYPE, lookup_expr="contains"
    )
    schedule_work = MultipleChoiceFilter(
        field_name="schedule_work", choices=SCHEDULE_WORK, lookup_expr="contains"
    )
    vacancy_status = ChoiceFilter(field_name="vacancy_status", choices=VACANCY_STATUS)
    required_experience = ChoiceFilter(
        field_name="required_experience", choices=EXPERIENCE
    )
    company = CharFilter(
        field_name="company",
        lookup_expr="exact",
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
            "skill_stack",
            "deadline",
        ]


class ResumeFilterSet(FilterSet):
    """Кастомный фильтр для резюме."""

    salary_expectations = filters.BaseCSVFilter(
        field_name="salary_expectations", lookup_expr="contains"
    )
    employment_type = MultipleChoiceFilter(
        field_name="employment_type", choices=EMPLOYMENT_TYPE, lookup_expr="contains"
    )
    schedule_work = MultipleChoiceFilter(
        field_name="schedule_work", choices=SCHEDULE_WORK, lookup_expr="contains"
    )
    education = ChoiceFilter(field_name="education", choices=EDUCATION)
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
            "pub_date",
            "education",
            "town",
            "citizenship",
            "bday",
            "work_experiences",
            "interview_status",
        ]


class CandidatesFilterSet(FilterSet):
    """Кастомный фильтр для кандидатов."""

    salary_expectations = filters.BaseCSVFilter(
        field_name="salary_expectations", lookup_expr="contains"
    )
    employment_type = MultipleChoiceFilter(
        field_name="employment_type", choices=EMPLOYMENT_TYPE, lookup_expr="contains"
    )
    schedule_work = MultipleChoiceFilter(
        field_name="schedule_work", choices=SCHEDULE_WORK, lookup_expr="contains"
    )
    education = ChoiceFilter(field_name="education", choices=EDUCATION)
    work_experiences = ChoiceFilter(field_name="work_experiences", choices=EXPERIENCE)
    interview_status = ChoiceFilter(
        field_name="interview_status", choices=INTERVIEW_STATUS
    )
    candidate_status = ChoiceFilter(
        field_name="candidate_status", choices=CANDIDATE_STATUS
    )

    class Meta:
        model = Candidate
        fields = [
            "first_name",
            "last_name",
            "city",
            "last_job",
            "cur_position",
            "vacancy",
            "salary_expectations",
            "employment_type",
            "schedule_work",
            "work_experiences",
            "pub_date",
            "education",
            "bday",
            "interview_status",
            "custom_status",
            "candidate_status",
        ]
