from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from .views import (
    CandidateViewSet,
    ChangePasswordView,
    CompanyViewSet,
    EmailConfirmationView,
    FunnelViewSet,
    LoginView,
    LogoutView,
    ResumeViewSet,
    SubStageViewSet,
    UserSignupView,
    UserViewSet,
    VacancyViewSet,
    NoteViewSet,
    CommentViewSet,
)

CONFIRM_URL = r"^confirm/(?P<user_id>[0-9]+)/(?P<confirmation_code>[0-9a-f-]+)/"

router = DefaultRouter()
router.register("vacancies", VacancyViewSet, basename="vacancies")
router.register("resumes", ResumeViewSet, basename="resumes")
router.register(r"candidates/(?P<candidate_id>\d+)/notes", NoteViewSet, basename="notes")
router.register(r"candidates/(?P<candidate_id>\d+)/notes/(?P<note_id>\d+)/comments", CommentViewSet, basename="comments")
router.register(
    r"vacancies/(?P<vacancy_id>\d+)/candidates", CandidateViewSet, basename="candidates"
)
router.register("companies", CompanyViewSet, basename="companies")
router.register("users", UserViewSet, basename="users")
router.register(r"candidates/(?P<candidate_id>\d+)/funnel", FunnelViewSet, "funnel")
router.register(
    r"candidates/(?P<candidate_id>\d+)/funnel/(?P<funnel_id>\d+)/substage",
    SubStageViewSet,
    "substage",
)

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("signup/", UserSignupView.as_view(), name="signup"),
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),
    re_path(CONFIRM_URL, EmailConfirmationView.as_view(), name="email_confirm"),
    path("", include(router.urls)),
]
