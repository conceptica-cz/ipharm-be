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
    "rest_framework.authtoken",
    "django_filters",
    "simple_history",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "corsheaders",
    "django_celery_beat",
    "common",
    "ipharm",
    "references",
    "updates",
    "users",
    "reports",
    "requisitions",
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
        "common.authentication.BearerTokenAuthentication",
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

# cors headers

CORS_ALLOW_ALL_ORIGINS = os.environ.get("CORS_ALLOW_ALL_ORIGINS") == "True"

if "CORS_ALLOWED_ORIGINS" in os.environ:
    CORS_ALLOWED_ORIGINS = [
        host.strip() for host in os.environ["CORS_ALLOWED_ORIGINS"].split(",")
    ]
else:
    CORS_ALLOWED_ORIGINS = []

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

TIME_ZONE = "CET"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

FILE_UPLOAD_MAX_MEMORY_SIZE = 3145728

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

APP_VERSION = (BASE_DIR / Path("version.txt")).read_text()

# CHANGE_HISTORY

CHANGE_HISTORY_MAX_INTERVAL = int(os.environ.get("CHANGE_HISTORY_MAX_INTERVAL", 500))

# REFERENCES AND UPDATES

BASE_ICISELNIKY_URL = os.environ.get(
    "BASE_ICISELNIKY_URL", "http://iciselniky-app:8000/api/v1"
)
ICISELNIKY_TOKEN = os.environ.get("ICISELNIKY_TOKEN", "")
BASE_IZADANKY_URL = os.environ.get(
    "BASE_IZADANKY_URL", "http://izadanky-app:8000/api/v1"
)
IZADANKY_TOKEN = os.environ.get("IZADANKY_TOKEN", "")
BASE_UNIS_URL = os.environ.get("BASE_UNIS_URL", "")
UNIS_TOKEN = os.environ.get("UNIS_TOKEN", "")
DEFAULT_DATA_LOADER = "updates.common.loaders.references_loader"
DEFAULT_MODEL_UPDATER = "updates.common.updaters.simple_model_updater"
DEFAULT_INCREMENTAL_UPDATE_INTERVAL = os.environ.get(
    "DEFAULT_INCREMENTAL_UPDATE_INTERVAL", 15
)
DEFAULT_FULL_UPDATE_INTERVAL = os.environ.get(
    "DEFAULT_INCREMENTAL_UPDATE_INTERVAL", 120
)
DEFAULT_RETRY_DELAY = os.environ.get("DEFAULT_RETRY_DELAY", 3600)

# if the time between the last patient care and the new care is less than this value
# (in hours), all care's related models will be migrated to the new care
MIGRATE_RELATED_TIME_GAP = os.environ.get("MIGRATE_RELATED_TIME_GAP", 36)

UPDATE_SOURCES = {
    "Clinic": {
        "data_loader_kwargs": {"url": BASE_ICISELNIKY_URL + "/clinics/"},
        "model_updater_kwargs": {
            "model": "references.Clinic",
            "identifiers": ["reference_id"],
        },
        "transformers": ["updates.common.transformers.id_to_reference_id"],
        "interval_incremental": 30,
        "interval_full": 120,
    },
    "Department": {
        "data_loader_kwargs": {"url": BASE_ICISELNIKY_URL + "/departments/"},
        "model_updater_kwargs": {
            "model": "references.Department",
            "identifiers": ["external_id"],
            "relations": {
                "clinic": {
                    "field": "clinic",
                    "key": "reference_id",
                    "delete_source_field": False,
                }
            },
        },
        "transformers": ["updates.common.transformers.delete_id"],
        "interval_incremental": 30,
        "interval_full": 120,
    },
    "Diagnosis": {
        "data_loader_kwargs": {"url": BASE_ICISELNIKY_URL + "/diagnoses/"},
        "model_updater_kwargs": {
            "model": "references.Diagnosis",
            "identifiers": ["code"],
        },
        "interval_incremental": 60,
        "interval_full": 240,
        "transformers": ["updates.common.transformers.delete_id"],
    },
    "Drug": {
        "data_loader_kwargs": {"url": BASE_ICISELNIKY_URL + "/drugs/"},
        "model_updater_kwargs": {
            "model": "references.Drug",
            "identifiers": ["code_sukl"],
        },
        "interval": os.environ.get("DRUG_UPDATE_INTERVAL", 60),
        "transformers": ["updates.common.transformers.delete_id"],
        "interval_incremental": 60,
        "interval_full": 240,
    },
    "ExternalDepartment": {
        "data_loader_kwargs": {"url": BASE_ICISELNIKY_URL + "/external-departments/"},
        "model_updater_kwargs": {
            "model": "references.ExternalDepartment",
            "identifiers": ["icp"],
        },
        "interval": os.environ.get("EXTERNAL_DEPARTMENT_UPDATE_INTERVAL", 60),
        "transformers": ["updates.common.transformers.delete_id"],
        "interval_incremental": 60,
        "interval_full": 240,
    },
    "Identification": {
        "data_loader_kwargs": {"url": BASE_ICISELNIKY_URL + "/identifications/"},
        "model_updater_kwargs": {
            "model": "references.Identification",
            "identifiers": ["identifier"],
        },
        "transformers": ["updates.common.transformers.delete_id"],
        "interval_incremental": 30,
        "interval_full": 120,
    },
    "InsuranceCompany": {
        "data_loader_kwargs": {"url": BASE_ICISELNIKY_URL + "/insurances/"},
        "model_updater_kwargs": {
            "model": "references.InsuranceCompany",
            "identifiers": ["code"],
        },
        "transformers": ["updates.common.transformers.delete_id"],
        "interval_incremental": 30,
        "interval_full": 120,
    },
    "MedicalFacility": {
        "data_loader_kwargs": {"url": BASE_ICISELNIKY_URL + "/facilities/"},
        "model_updater_kwargs": {
            "model": "references.MedicalFacility",
            "identifiers": ["facility_id"],
        },
        "transformers": ["updates.common.transformers.delete_id"],
        "interval_incremental": 60,
        "interval_full": 240,
    },
    "Person": {
        "data_loader_kwargs": {"url": BASE_ICISELNIKY_URL + "/persons/"},
        "model_updater_kwargs": {
            "model": "references.Person",
            "identifiers": ["person_number"],
        },
        "transformers": ["updates.common.transformers.delete_id"],
        "interval_incremental": 30,
        "interval_full": 120,
    },
    "Patient": {
        "data_loader": "updates.bulovka.loaders.patient_loader",
        "data_loader_kwargs": {
            "url": BASE_UNIS_URL
            + os.environ.get("PATIENT_URL_PATH", "/patient/hospitalized/"),
            "token": UNIS_TOKEN,
        },
        "transformers": ["updates.bulovka.transformers.patient_transformer"],
        "post_operations": [
            "updates.bulovka.post_operations.update_names",
            "updates.bulovka.post_operations.finish_cares",
        ],
        "model_updater": "updates.bulovka.updaters.patient_updater",
        "by_clinic": True,
        "queue": "medium_priority",
        "interval_incremental": 60,
        "interval_full": 240,
    },
    "Requisition": {
        "data_loader_kwargs": {
            "url": BASE_IZADANKY_URL + "/requisitions/?is_synced=false&type=ipharm",
            "token": IZADANKY_TOKEN,
        },
        "model_updater": "updates.requisitions.updaters.update_requisition",
        "transformers": [],
        "queue": "medium_priority",
        "interval_full": 15,
    },
}
# REQUISITION

UPDATE_REQUISITION_URL = BASE_IZADANKY_URL + "/requisitions/{id}/"

# REPORTS

INSURANCE_REPORT_FOLDER = "dosages"
GENERIC_REPORT_FOLDER = "reports"

GENERIC_REPORTS = {
    "uzis": {
        "description": "UZIS výkaz",
        "file_name": "uzis_report",
        "time_ranges": ["year"],
        "filters": [],
        "data_loader": "reports.generic_reports.uzis.uzis_loader",
        "renderers": {
            "pdf": {
                "renderer": "reports.generic_reports.pdf.pdf_renderer",
                "renderer_kwargs": {
                    "template": "generic_reports/uzis/pdf.html",
                },
            },
        },
        "order": 1,
        "variables": [
            {
                "name": "clinical_pharmacist_persons",
                "description": "Klinický farmaceut se specializací - fyzické osoby",
                "variable_type": "int",
                "value": "0",
                "order": 0,
            },
            {
                "name": "clinical_pharmacist_jobs",
                "description": "Klinický farmaceut se specializací - počet úvazků",
                "variable_type": "int",
                "value": "0",
                "order": 1,
            },
            {
                "name": "pre_clinical_pharmacist_persons",
                "description": "Klinický farmaceut zařazený do předatestační přípravy - fyzické osoby",
                "variable_type": "int",
                "value": "0",
                "order": 2,
            },
            {
                "name": "pre_clinical_pharmacist_jobs",
                "description": "Klinický farmaceut zařazený do předatestační přípravy - počet úvazků",
                "variable_type": "int",
                "value": "0",
                "order": 3,
            },
            {
                "name": "department_of_cp_high_level",
                "description": "Oddělení klinické farmacie vyššího typu",
                "variable_type": "bool",
                "value": "False",
                "order": 4,
            },
            {
                "name": "department_of_cp_base_level",
                "description": "Oddělení klinické farmacie základního typu",
                "variable_type": "bool",
                "value": "False",
                "order": 5,
            },
            {
                "name": "workplace_of_cp",
                "description": "Pracoviště klinického farmaceuta",
                "variable_type": "bool",
                "value": "False",
                "order": 6,
            },
            {
                "name": "consultation_workplace_of_cp",
                "description": "Pracoviště s konzultační službou klinického farmaceuta",
                "variable_type": "bool",
                "value": "False",
                "order": 7,
            },
            {
                "name": "ministry",
                "description": "Ministerstvo",
                "variable_type": "bool",
                "value": "False",
                "order": 8,
            },
            {
                "name": "region",
                "description": "Kraj",
                "variable_type": "bool",
                "value": "False",
                "order": 9,
            },
            {
                "name": "city",
                "description": "Město/obec",
                "variable_type": "bool",
                "value": "False",
                "order": 10,
            },
            {
                "name": "person",
                "description": "Fyzická osoba/církev",
                "variable_type": "bool",
                "value": "False",
                "order": 11,
            },
            {
                "name": "acute_care_beds",
                "description": "Lůžka akutní péče",
                "variable_type": "int",
                "value": "0",
                "order": 12,
            },
            {
                "name": "intensive_care",
                "description": "Lůžka intenzivní péče",
                "variable_type": "int",
                "value": "0",
                "order": 14,
            },
            {
                "name": "surgical_beds",
                "description": "Lůžka chirurgických oborů",
                "variable_type": "int",
                "value": "0",
                "order": 15,
            },
            {
                "name": "internal_medicine_beds",
                "description": "Lůžka interních oborů",
                "variable_type": "int",
                "value": "0",
                "order": 16,
            },
            {
                "name": "aftercare_beds",
                "description": "Lůžka následné péče",
                "variable_type": "int",
                "value": "0",
                "order": 17,
            },
            {
                "name": "long_term_care_beds",
                "description": "Lůžka dlouhodobé péče",
                "variable_type": "int",
                "value": "0",
                "order": 18,
            },
            {
                "name": "internal_ambulances",
                "description": "Specializovaná ambulantní složka zdravotnického zařízení lůžkové péče",
                "variable_type": "int",
                "value": "0",
                "order": 19,
            },
            {
                "name": "independent_physician",
                "description": "Samostatná ordinace (fyzická/právnická osoba)",
                "variable_type": "int",
                "value": "0",
                "order": 20,
            },
            {
                "name": "surgical_clinics",
                "description": "Chirurgické obory",
                "variable_type": "int",
                "value": "0",
                "order": 21,
            },
            {
                "name": "internal_clinics",
                "description": "Interní obory",
                "variable_type": "int",
                "value": "0",
                "order": 22,
            },
            {
                "name": "oncology_clinics",
                "description": "Onkologie, paliativní medicína",
                "variable_type": "int",
                "value": "0",
                "order": 23,
            },
            {
                "name": "psychiatry_clinics",
                "description": "Psychiatrie, geriatrie",
                "variable_type": "int",
                "value": "0",
                "order": 24,
            },
            {
                "name": "aro_icu",
                "description": "Anesteziologie a intenzivní medicína (ARO, JIP)",
                "variable_type": "int",
                "value": "0",
                "order": 25,
            },
            {
                "name": "author",
                "description": "Výkaz vyplnil",
                "variable_type": "str",
                "value": "",
                "order": 27,
            },
            {
                "name": "author_phone",
                "description": "Telefon",
                "variable_type": "str",
                "value": "",
                "order": 28,
            },
            {
                "name": "author_email",
                "description": "E-mail",
                "variable_type": "str",
                "value": "",
                "order": 29,
            },
        ],
    },
    "risk_levels": {
        "description": "Rizikovost",
        "file_name": "Rizikovost",
        "time_ranges": ["year", "month", "custom"],
        "filters": ["clinic", "department", "care_type"],
        "data_loader": "reports.generic_reports.statistical_reports.risk_level_loader",
        "renderers": {
            "pdf": {
                "renderer": "reports.generic_reports.pdf.pdf_renderer",
                "renderer_kwargs": {
                    "template": "generic_reports/statistical_reports/risk_levels_pdf.html",  # noqa
                },
            },
            "xlsx": {
                "renderer": "reports.generic_reports.xlsx.xlsx_renderer",
                "renderer_kwargs": {
                    "data_transformer": "reports.generic_reports.statistical_reports.risk_level_xlsx_data_transformer",  # noqa
                },
            },
        },
        "order": 2,
    },
    "pharmacological_evaluation_patients": {
        "description": "FTD hodnocení – pacienti",
        "file_name": "FTD hodnocení – pacienti",
        "time_ranges": ["year", "month", "custom"],
        "filters": ["clinic", "department", "care_type"],
        "data_loader": "reports.generic_reports.statistical_reports.evaluation_patients_loader",  # noqa
        "renderers": {
            "pdf": {
                "renderer": "reports.generic_reports.pdf.pdf_renderer",
                "renderer_kwargs": {
                    "template": "generic_reports/statistical_reports/evaluation_patients_pdf.html",  # noqa
                },
            },
            "xlsx": {
                "renderer": "reports.generic_reports.xlsx.xlsx_renderer",
                "renderer_kwargs": {
                    "data_transformer": "reports.generic_reports.statistical_reports.evaluation_patients_xlsx_data_transformer",  # noqa
                },
            },
        },
        "order": 3,
    },
    "tags": {
        "description": "Štítky",
        "file_name": "Štítky",
        "time_ranges": ["year", "month", "custom", "care_type"],
        "filters": ["clinic", "department"],
        "data_loader": "reports.generic_reports.statistical_reports.tags_loader",
        "renderers": {
            "pdf": {
                "renderer": "reports.generic_reports.pdf.pdf_renderer",
                "renderer_kwargs": {
                    "template": "generic_reports/statistical_reports/tags_pdf.html",  # noqa
                },
            },
            "xlsx": {
                "renderer": "reports.generic_reports.xlsx.xlsx_renderer",
                "renderer_kwargs": {
                    "data_transformer": "reports.generic_reports.statistical_reports.tags_xlsx_data_transformer",  # noqa
                },
            },
        },
        "order": 4,
    },
    "pharmacological_evaluation_drugs": {
        "description": "FTD hodnocení – léčiva",
        "file_name": "FTD hodnocení – léčiva",
        "time_ranges": ["year", "month", "custom"],
        "filters": ["clinic", "department", "atc_group_exact"],
        "data_loader": "reports.generic_reports.statistical_reports.evaluation_drugs_loader",  # noqa
        "renderers": {
            "xlsx": {
                "renderer": "reports.generic_reports.xlsx.xlsx_renderer",
                "renderer_kwargs": {
                    "data_transformer": "reports.generic_reports.statistical_reports.evaluation_drugs_xlsx_data_transformer",  # noqa
                },
            },
        },
        "order": 5,
    },
    "pharmacological_evaluation_groups": {
        "description": "ATC skupiny souhrn",
        "file_name": "ATC skupiny souhrn",
        "time_ranges": ["year", "month", "custom"],
        "filters": ["clinic", "department", "atc_group_startswith"],
        "data_loader": "reports.generic_reports.statistical_reports.evaluation_groups_loader",  # noqa
        "renderers": {
            "xlsx": {
                "renderer": "reports.generic_reports.xlsx.xlsx_renderer",
                "renderer_kwargs": {
                    "data_transformer": "reports.generic_reports.statistical_reports.evaluation_groups_xlsx_data_transformer",  # noqa
                },
            },
        },
        "order": 6,
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
CELERY_TASK_ALWAYS_EAGER = False

CELERY_TASK_DEFAULT_QUEUE = "low_priority"
CELERY_TASK_ROUTES = {
    "updates.tasks.update": {"queue": "medium_priority"},
    "requisitions.tasks.load_patient_task": {"queue": "high_priority"},
}


# LOGGING

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(levelname)s %(asctime)s %(name)s %(filename)s %(lineno)s %(funcName)s %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "json",
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
        "ipharm": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
        },
        "references": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
        },
        "reports": {
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

# DJANGO DEBUG TOOLBAR
if ENVIRONMENT == "development":
    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
    DEBUG_TOOLBAR_PANELS = [
        "debug_toolbar.panels.versions.VersionsPanel",
        "debug_toolbar.panels.timer.TimerPanel",
        "debug_toolbar.panels.settings.SettingsPanel",
        "debug_toolbar.panels.headers.HeadersPanel",
        "debug_toolbar.panels.request.RequestPanel",
        "debug_toolbar.panels.sql.SQLPanel",
        "debug_toolbar.panels.staticfiles.StaticFilesPanel",
        "debug_toolbar.panels.templates.TemplatesPanel",
        "debug_toolbar.panels.cache.CachePanel",
        "debug_toolbar.panels.signals.SignalsPanel",
        "debug_toolbar.panels.logging.LoggingPanel",
        "debug_toolbar.panels.redirects.RedirectsPanel",
    ]
    #    DEBUG_TOOLBAR_CONFIG = {"RESULTS_CACHE_SIZE": 0}

    import socket  # only if you haven't already imported this

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + [
        "127.0.0.1",
        "10.0.2.2",
    ]
