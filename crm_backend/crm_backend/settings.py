import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(os.path.join(BASE_DIR.parent, "infra/.env"))

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = os.getenv("DEBUG", default=True)

ALLOWED_HOSTS = [
    "backend",
    "localhost",
    "127.0.0.1",
    "80.87.107.166",
    "80.87.109.74",
    "80.87.109.82",
    "80.87.109.248",
    "80.87.109.8",
    "80.87.109.229",
    "meetingroom.acceleratorpracticum.ru",
    "bugaton1.acceleratorpracticum.ru",
    "bugaton2.acceleratorpracticum.ru",
    "bugaton3.acceleratorpracticum.ru",
    "bugaton4.acceleratorpracticum.ru",
    "bugaton5.acceleratorpracticum.ru",
]


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "recruitment.apps.RecruitmentConfig",
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
    "users",
    "api",
    "multiselectfield",
    "django_filters",
    "drf_spectacular",
    "drf_spectacular_sidecar",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "crm_backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "crm_backend.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": os.getenv(
            "DB_ENGINE",
            default="django.db.backends.postgresql",
        ),
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
    {
        "NAME": "users.validators.CustomPasswordValidator",
    },
]

AUTH_USER_MODEL = "users.User"


LANGUAGE_CODE = "ru-RU"

TIME_ZONE = "Europe/Volgograd"

USE_I18N = True

USE_TZ = True


STATIC_URL = "/static_backend/"
STATIC_ROOT = os.path.join(BASE_DIR, "static_backend")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "api.authentication.CustomAuthentication",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "MeetingRoom",
    "DESCRIPTION": "API CRM платформы управления процессом найма для HR.",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SWAGGER_UI_DIST": "SIDECAR",
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "SWAGGER_UI_SETTINGS": {
        "filter": True,
    },
    "COMPONENT_SPLIT_REQUEST": True,
    "REDOC_DIST": "SIDECAR",
}

# CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://localhost:3000",
    "https://127.0.0.1:3000",
    "https://80.87.107.166:3000",
    "https://80.87.109.74:3000",
    "https://80.87.109.82:3000",
    "https://80.87.109.248:3000",
    "https://80.87.109.8:3000",
    "https://80.87.109.229:3000",
    "https://meetingroom.acceleratorpracticum.ru:3000",
    "https://bugaton1.acceleratorpracticum.ru:3000",
    "https://bugaton2.acceleratorpracticum.ru:3000",
    "https://bugaton3.acceleratorpracticum.ru:3000",
    "https://bugaton4.acceleratorpracticum.ru:3000",
    "https://bugaton5.acceleratorpracticum.ru:3000",
]

CORS_ALLOW_CREDENTIALS = True

SESSION_COOKIE_AGE = 60 * 60 * 24 * 7  # 1 week
SESSION_COOKIE_SAMESITE = "None"
SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SAMESITE = "None"
CSRF_COOKIE_SECURE = True

CSRF_TRUSTED_ORIGINS = [
    "https://backend",
    "http://localhost:3000",
    "http://127.0.0.1",
    "https://localhost",
    "https://127.0.0.1",
    "https://80.87.107.166",
    "https://80.87.109.74",
    "https://80.87.109.82",
    "https://80.87.109.248",
    "https://80.87.109.8",
    "https://80.87.109.229",
    "https://meetingroom.acceleratorpracticum.ru",
    "https://bugaton1.acceleratorpracticum.ru",
    "https://bugaton2.acceleratorpracticum.ru",
    "https://bugaton3.acceleratorpracticum.ru",
    "https://bugaton4.acceleratorpracticum.ru",
    "https://bugaton5.acceleratorpracticum.ru",
]

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=10),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(days=1),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
    # custom
    "AUTH_COOKIE": "access_token",  # Cookie name. Enables cookies if value is set.
    "AUTH_COOKIE_DOMAIN": None,  # A string like "example.com", or None for standard domain cookie.
    "AUTH_COOKIE_SECURE": True,  # Whether the auth cookies should be secure (https:// only).
    "AUTH_COOKIE_HTTP_ONLY": True,  # Http only cookie flag.It"s not fetch by javascript.
    "AUTH_COOKIE_PATH": "/",  # The path of the auth cookie.
    "AUTH_COOKIE_SAMESITE": "None",  # Whether to set the flag restricting cookie leaks on cross-site requests. This can be "Lax", "Strict", or None to disable the flag.
}

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = os.path.join(BASE_DIR, "sent_emails")
DOMAIN_NAME = "meetingroom.acceleratorpracticum.ru"
EMAIL_HOST_USER = "noreply@" + DOMAIN_NAME

TELEGRAM_CHAT_ID = os.getenv("TG_CHAT_ID")
TELEGRAM_TOKEN = os.getenv("TG_TOKEN")
