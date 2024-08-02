from pathlib import Path
from decouple import config
import os
import sys

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, os.path.join(BASE_DIR, "apps"))

SECRET_KEY = config("SECRET_KEY")


LOCAL_APPS = [
    "apps.core.apps.CoreConfig",
    "apps.users.apps.UsersConfig",
]
THIRD_PARTY_APPS = [
    "rest_framework",
    "drf_spectacular",
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    *LOCAL_APPS,
    *THIRD_PARTY_APPS,
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

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

WSGI_APPLICATION = "config.wsgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file_info": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/info.log"),
            "formatter": "verbose",
        },
        "file_critical": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/critical.log"),
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file_info", "file_critical"],
            "level": "INFO",
            "propagate": True,
        },
    },
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": config("CACHE_DB_URL"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

# Email configs
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config("EMAIL_HOST")
EMAIL_HOST_USER = config("EMAIL_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_PASSWORD")
EMAIL_PORT = config("EMAIL_PORT")
DEFAULT_FROM_EMAIL = config("EMAIL_FROM")


AUTH_USER_MODEL = "users.User"

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "FoodAnywhere Api Docs",
    "DESCRIPTION": "The description intentionally left blank.",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}
