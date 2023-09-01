from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from .views import (
    EmailConfirmationView,
    LoginView,
    LogoutView,
    ResumeViewSet,
    UserSignupView,
    VacancyViewSet,
)

CONFIRM_URL = r"^confirm/(?P<user_id>[0-9]+)/(?P<confirmation_code>[0-9a-f-]+)/"

router = DefaultRouter()
router.register("vacancies", VacancyViewSet, basename="vacancies")
router.register("resumes", ResumeViewSet, basename="resumes")

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("signup/", UserSignupView.as_view(), name="signup"),
    re_path(CONFIRM_URL, EmailConfirmationView.as_view(), name="email_confirm"),
    path("", include(router.urls)),
]
