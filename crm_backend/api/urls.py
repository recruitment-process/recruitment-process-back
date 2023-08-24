from django.urls import path, re_path

from .views import EmailConfirmationView, LoginView, UserSignupView

CONFIRM_URL = (
    r"^confirm/(?P<email>[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]{1,}\.[a-zA-Z]{2,})"
    "/(?P<confirmation_code>[0-9a-f-]+)/"
)

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("signup/", UserSignupView.as_view(), name="signup"),
    re_path(CONFIRM_URL, EmailConfirmationView.as_view(), name="email_confirm"),
]
