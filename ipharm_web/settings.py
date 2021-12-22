"""
Django settings for ipharm_web project.

Generated by 'django-admin startproject' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
import sys
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "apps"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG") == "True"
ENVIRONMENT = os.environ.get("ENVIRONMENT", "production")

if "ALLOWED_HOSTS" in os.environ:
    ALLOWED_HOSTS = [host.strip() for host in os.environ["ALLOWED_HOSTS"].split(",")]
else:
    ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    "rest_framework",
    "django_filters",
    "simple_history",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "django_celery_beat",
    "common",
    "ipharm",
    "references",
    "updates",
    "users",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
]

ROOT_URLCONF = "ipharm_web.urls"

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

WSGI_APPLICATION = "ipharm_web.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["POSTGRES_DB"],
        "USER": os.environ["POSTGRES_USER"],
        "PASSWORD": os.environ["POSTGRES_PASSWORD"],
        "HOST": os.environ["POSTGRES_HOST"],
        "PORT": os.environ["POSTGRES_PORT"],
    }
}

AUTH_USER_MODEL = "users.User"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 100,
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "SWAGGER_UI_DIST": "SIDECAR",
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
    "TITLE": "iPharm API",
    "DESCRIPTION": "iPharm application REST API",
    "VERSION": "1",
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

APP_VERSION = Path("version.txt").read_text()

# REFERENCES AND UPDATES

BASE_REFERENCES_URL = os.environ.get(
    "BASE_REFERENCES_URL", "http://iciselniky-app:8000/api/v1"
)
BASE_PATIENT_URL = os.environ["BASE_PATIENT_URL"]
REFERENCES_TOKEN = os.environ["REFERENCES_TOKEN"]
DEFAULT_DATA_LOADER = "updates.common.loaders.references_loader"
DEFAULT_TRANSFORMERS = ["updates.common.transformers.delete_id"]
DEFAULT_MODEL_UPDATER = "updates.common.updaters.simple_model_updater"
DEFAULT_INCREMENTAL_UPDATE_INTERVAL = os.environ.get(
    "DEFAULT_INCREMENTAL_UPDATE_INTERVAL", 15
)
DEFAULT_FULL_UPDATE_INTERVAL = os.environ.get(
    "DEFAULT_INCREMENTAL_UPDATE_INTERVAL", 120
)
UPDATE_SOURCES = {
    "Clinic": {
        "data_loader_kwargs": {"url": BASE_REFERENCES_URL + "/clinics/"},
        "model_updater_kwargs": {
            "model": "references.Clinic",
            "identifiers": ["external_id"],
        },
    },
    "Department": {
        "data_loader_kwargs": {"url": BASE_REFERENCES_URL + "/departments/"},
        "model_updater_kwargs": {
            "model": "references.Department",
            "identifiers": ["external_id"],
            "relations": {
                "clinic_external_id": {"field": "clinic", "key": "external_id"}
            },
        },
    },
    "Diagnosis": {
        "data_loader_kwargs": {"url": BASE_REFERENCES_URL + "/diagnoses/"},
        "model_updater_kwargs": {
            "model": "references.Diagnosis",
            "identifiers": ["code"],
        },
        "interval": os.environ.get("DIAGNOSIS_UPDATE_INTERVAL", 60),
    },
    "Drug": {
        "data_loader_kwargs": {"url": BASE_REFERENCES_URL + "/drugs/"},
        "model_updater_kwargs": {
            "model": "references.Drug",
            "identifiers": ["code_sukl"],
        },
        "interval": os.environ.get("DRUG_UPDATE_INTERVAL", 60),
    },
    "Identification": {
        "data_loader_kwargs": {"url": BASE_REFERENCES_URL + "/identifications/"},
        "model_updater_kwargs": {
            "model": "references.Identification",
            "identifiers": ["identifier"],
        },
    },
    "InsuranceCompany": {
        "data_loader_kwargs": {"url": BASE_REFERENCES_URL + "/insurances/"},
        "model_updater_kwargs": {
            "model": "references.InsuranceCompany",
            "identifiers": ["code"],
        },
    },
    "MedicalFacility": {
        "data_loader_kwargs": {"url": BASE_REFERENCES_URL + "/facilities/"},
        "model_updater_kwargs": {
            "model": "references.MedicalFacility",
            "identifiers": ["facility_id"],
        },
        "interval": os.environ.get("FACILITIES_UPDATE_INTERVAL", 60),
    },
    "Person": {
        "data_loader_kwargs": {"url": BASE_REFERENCES_URL + "/persons/"},
        "model_updater_kwargs": {
            "model": "references.Person",
            "identifiers": ["person_number"],
        },
    },
    "Patient": {
        "data_loader": "updates.bulovka.loaders.patient_loader",
        "data_loader_kwargs": {"url": BASE_PATIENT_URL + "/patient/"},
        "transformers": ["updates.bulovka.transformers.patient_transformer"],
        "model_updater": "updates.bulovka.updaters.patient_updater",
        "by_clinic": True,
    },
}

# CELERY
CELERY_TIMEZONE = TIME_ZONE
REDIS_HOST = os.environ["REDIS_HOST"]
REDIS_PORT = os.environ.get("REDIS_PORT", 6379)
CELERY_BROKER_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/1"
CELERY_BROKER_TRANSPORT_OPTIONS = {
    "visibility_timeout": float("inf"),
    "result_chord_ordered": True,
}
CELERY_RESULT_BACKEND = f"redis://{REDIS_HOST}:{REDIS_PORT}/2"
CELERY_TASK_IGNORE_RESULT = True
CELERY_TASK_ACKS_LATE = True

# REFERENCES
OUR_HEALTH_CARE_IDENTIFIER = os.environ.get("OUR_HEALTH_CARE_IDENTIFIER", 1)

# LOGGING

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "django.request": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "django.db.backends": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "common": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
        },
        "references": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
        },
        "updates": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
        },
        "users": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
        },
    },
}

# SENTRY

if os.environ.get("SENTRY_DSN"):
    import sentry_sdk
    from sentry_sdk.integrations.celery import CeleryIntegration
    from sentry_sdk.integrations.django import DjangoIntegration

    SENTRY_DSN = os.environ["SENTRY_DSN"]
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration(), CeleryIntegration()],
        environment=os.environ.get("SENTRY_ENVIRONMENT", "production"),
        release=APP_VERSION,
    )

# DJANGO EXTENSIONS
if ENVIRONMENT == "development":
    INSTALLED_APPS += ["django_extensions"]
