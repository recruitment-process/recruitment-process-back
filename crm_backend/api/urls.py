from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import LoginView, ResumeViewSet, VacancyViewSet

router = DefaultRouter()
router.register("vacancies", VacancyViewSet, basename="vacancies")
router.register("resumes", ResumeViewSet, basename="resumes")

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("", include(router.urls)),
]
