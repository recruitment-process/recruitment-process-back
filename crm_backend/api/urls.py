from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from .views import (
    EmailConfirmationView,
    LoginView,
    ResumeViewSet,
    UserSignupView,
    VacancyViewSet,
    NoteViewSet,
    CommentViewSet,
)

CONFIRM_URL = (
    r"^confirm/(?P<email>[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]{1,}\.[a-zA-Z]{2,})"
    "/(?P<confirmation_code>[0-9a-f-]+)/"
)

router = DefaultRouter()
router.register("vacancies", VacancyViewSet, basename="vacancies")
router.register("resumes", ResumeViewSet, basename="resumes")
router.register(r"candidates/(?P<candidate_id>\d+)/notes", NoteViewSet, basename="notes")
router.register(r"candidates/(?P<candidate_id>\d+)/notes/(?P<note_id>\d+)/comments", CommentViewSet, basename="comments")

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("signup/", UserSignupView.as_view(), name="signup"),
    re_path(CONFIRM_URL, EmailConfirmationView.as_view(), name="email_confirm"),
    path("", include(router.urls)),
]
