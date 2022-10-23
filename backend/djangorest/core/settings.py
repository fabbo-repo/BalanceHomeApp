"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
from configurations import Configuration
from django.utils.timezone import timedelta
import os
import dj_database_url
from django.utils.translation import gettext_lazy as _

def get_env(environ_name, default_value=None):
    return os.environ.get(environ_name) or default_value

def get_int_env(environ_name, default_value=None):
    return int(os.environ.get(environ_name) or default_value)

def get_bool_env(environ_name, default_value=None):
    if not os.environ.get(environ_name): return default_value
    if os.environ.get(environ_name).lower() in ['true', '1', 't', 'y', 'yes']: return True
    return False

def get_list_env(environ_name, default_value=None):
    if not os.environ.get(environ_name): return default_value
    return os.environ.get(environ_name).split(',')

class Dev(Configuration):
    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path(__file__).resolve().parent.parent

    DOMAIN = get_env('APP_DOMAIN', '127.0.0.1')
    PORT = get_env('APP_PORT', '8000')
    BASE_URL = DOMAIN + ':' + PORT

    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = 'django-insecure-5bmqrmx9io3#onh8t9am()96q82!npe9&-m57c+3&6=4b2u-u-'

    # True by default but have the option to set it false with an environment variable
    DEBUG = get_bool_env('APP_DEBUG', True)

    ALLOWED_HOSTS = [ '*' ]
    CORS_ALLOW_ALL_ORIGINS = True
    # X_FRAME_OPTIONS = 'ALLOW-FROM ' + os.environ.get('HOSTNAME')
    # CSRF_COOKIE_SAMESITE = None
    # CSRF_TRUSTED_ORIGINS = [os.environ.get('HOSTNAME')]
    # CSRF_COOKIE_SECURE = True
    # SESSION_COOKIE_SECURE = True
    # CSRF_COOKIE_SAMESITE = 'None'
    # SESSION_COOKIE_SAMESITE = 'None'

    # Application definition

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        # Cors:
        "corsheaders",
        # Admin documentation:
        'django.contrib.admindocs',
        # Rest framework:
        'rest_framework',
        'django_filters',
        # Swager:
        'drf_yasg',
        # Task schedulling:
        'django_celery_results',
        'django_celery_beat',
        # Backup
        'dbbackup',
        # Custom apps:
        'custom_auth',
        'balance',
        'revenue',
        'expense',
        'coin',
        'frontend_version'
    ]

    MIDDLEWARE = [
        "corsheaders.middleware.CorsMiddleware",
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.locale.LocaleMiddleware',
        'django.middleware.common.CommonMiddleware',
        #'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    ROOT_URLCONF = 'core.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]

    WSGI_APPLICATION = 'core.wsgi.application'


    # Database
    # https://docs.djangoproject.com/en/4.1/ref/settings/#databases

    # conn_max_age is the lifetime of a database connection in seconds
    DATABASES = {'default': dj_database_url.config(
        default='sqlite:///'+os.path.join(BASE_DIR, 'default.sqlite3'),
        conn_max_age=600
    )}


    # Password validation
    # https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]


    # Internationalization
    # https://docs.djangoproject.com/en/4.1/topics/i18n/

    LANGUAGE_CODE = 'en'
    LOCALE_PATHS = [
        BASE_DIR / 'locale/',
    ]
    LANGUAGES = (
        ('en', _('English')),
        ('es', _('Spanish')),
    )

    TIME_ZONE = "UTC"
    # Enables Django’s translation system
    USE_I18N = True
    # Django will display numbers and dates using the format of the current locale
    USE_L10N = True
    # Datetimes will be timezone-aware
    USE_TZ = True


    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/4.1/howto/static-files/

    STATIC_URL = 'static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')

    MEDIA_URL = 'media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

    # Default primary key field type
    # https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
                "style": "{",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "verbose",
            },
        },
        "root": {
            "handlers": ["console"],
            "level": "DEBUG",
        }
    }

    # Backup
    DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
    DBBACKUP_STORAGE_OPTIONS = {'location': '.'}

    # Django Rest Framework setting:
    REST_FRAMEWORK = {
        "DEFAULT_AUTHENTICATION_CLASSES": [
            "rest_framework_simplejwt.authentication.JWTAuthentication"
        ],
        "DEFAULT_PERMISSION_CLASSES": [
            "rest_framework.permissions.IsAuthenticated",
        ],
        "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
        "PAGE_SIZE": 10,
        "DEFAULT_FILTER_BACKENDS": [
            "django_filters.rest_framework.DjangoFilterBackend",
        ],
    }

    SIMPLE_JWT = {
        "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
        "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    }

    SWAGGER_SETTINGS = {
        "SECURITY_DEFINITIONS": {
            "Token": {
                "type": "apiKey", 
                "name": "Authorization",
                "in": "header"
            },
            "Basic": {
                "type": "basic"
            },
        }
    }

    AUTH_USER_MODEL = "custom_auth.User"

    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    CELERY_RESULT_BACKEND = "django-db"
    CELERY_BROKER_URL = "redis://localhost:6379/0"

    # Time to wait for a new email verification code generation 
    EMAIL_CODE_THRESHOLD = get_int_env('APP_EMAIL_CODE_THRESHOLD', 120)
    # Email verification code validity duration
    EMAIL_CODE_VALID = get_int_env('APP_EMAIL_CODE_VALID', 120)

    COIN_TYPE_CODES = get_list_env('COIN_TYPE_CODES', ['EUR', 'USD'])

class Prod(Dev):
    DEBUG = False
    
    DOMAIN = get_env('APP_DOMAIN', '127.0.0.1')
    PORT = get_env('APP_PORT', '80')
    #SECRET_KEY = get_env('DJANGO_SECRET_KEY', os.urandom(20).hex())
    SECRET_KEY = os.urandom(20).hex()
    ALLOWED_HOSTS = get_list_env('APP_ALLOWED_HOSTS', 
        [ "localhost", "0.0.0.0" ])
    if get_list_env("APP_CORS_ALLOWED_HOSTS"):
        CORS_ALLOW_ALL_ORIGINS = False
        CORS_ALLOWED_ORIGINS = get_list_env("APP_CORS_ALLOWED_HOSTS")
    CSRF_TRUSTED_ORIGINS = get_list_env("APP_CORS_ALLOWED_HOSTS", 
        [ "http://localhost:8000", "http://127.0.0.1:8000" ]
    )
        
    # Backup
    DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
    DBBACKUP_STORAGE_OPTIONS = {'location': '/var/backup'}
    DBBACKUP_GPG_RECIPIENT = get_env('DBBACKUP_GPG_RECIPIENT', None)
    DBBACKUP_GPG_ALWAYS_TRUST = True
    
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
                "style": "{",
            },
        },
        "handlers": {
            "logfile": {
                "class": "logging.FileHandler",
                "filename": "/var/log/balance_app/app.log",
                "formatter": "verbose",
            },
        },
        "root": {
            "handlers": ["logfile"],
            "level": "ERROR",
        }
    }
    
    SIMPLE_JWT = {
        "ACCESS_TOKEN_LIFETIME": timedelta(hours=1),
        "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    }

    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    # It is setup for gmail
    EMAIL_HOST = get_env('APP_EMAIL_HOST', 'smtp.gmail.com')
    EMAIL_USE_TLS = True
    EMAIL_PORT = get_int_env('APP_EMAIL_PORT', 587)
    EMAIL_HOST_USER = get_env('APP_EMAIL_HOST_USER', 'example@gmail.com')
    EMAIL_HOST_PASSWORD = get_env('APP_EMAIL_HOST_PASSWORD', 'password')
    
    CELERY_BROKER_URL = get_env('APP_CELERY_BROKER_URL', "redis://localhost:6379/0")
