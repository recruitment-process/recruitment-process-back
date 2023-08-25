from django_filters import FilterSet, filters
from recruitment.models import Vacancy


class VacancyFilterSet(FilterSet):
    """Кастомный фильтр для зарплат."""

    salary = filters.BaseCSVFilter(field_name="salary", lookup_expr="contains")

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
