"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
from configurations import Configuration, values
import dj_database_url
from datetime import timedelta
import os

class Dev(Configuration):
    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path(__file__).resolve().parent.parent

    APP_DOMAIN = str(values.Value('127.0.0.1'))
    APP_PORT = str(values.Value('8000'))
    BASE_URL = APP_DOMAIN + ':' + APP_PORT

    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = 'django-insecure-5bmqrmx9io3#onh8t9am()96q82!npe9&-m57c+3&6=4b2u-u-'

    # True by default but have the option to set it false with an environment variable
    DEBUG = values.BooleanValue(True)

    ALLOWED_HOSTS = [ '*' ]
    # X_FRAME_OPTIONS = 'ALLOW-FROM ' + os.environ.get('HOSTNAME')
    # CSRF_COOKIE_SAMESITE = None
    # CSRF_TRUSTED_ORIGINS = [os.environ.get('HOSTNAME')]
    CSRF_TRUSTED_ORIGINS = [ 
        "http://localhost", 
        "http://127.0.0.1", 
        "https://localhost", 
        "https://127.0.0.1" 
    ]
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
        'rest_framework',
        'django_filters',
        'drf_yasg',
        # Custom apps:
        'custom_auth'
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
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

    DATABASES = values.DatabaseURLValue(
        f"sqlite:///{BASE_DIR}/db.sqlite3"
    )


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

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = values.Value("UTC")

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True


    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/4.1/howto/static-files/

    STATIC_URL = 'static/'

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

    # Django Rest Framework setting:
    REST_FRAMEWORK = {
        "DEFAULT_AUTHENTICATION_CLASSES": [
            "rest_framework_simplejwt.authentication.JWTAuthentication"
        ],
        "DEFAULT_PERMISSION_CLASSES": [
            "rest_framework.permissions.IsAuthenticated",
        ],
        "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
        "PAGE_SIZE": 100,
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

class Prod(Dev):
    DEBUG = False
    APP_DOMAIN = str(values.Value('127.0.0.1'))
    APP_PORT = str(values.Value('80'))
    SECRET_KEY = values.SecretValue()
    ALLOWED_HOSTS = values.ListValue([ "localhost", "0.0.0.0" ])
    CSRF_TRUSTED_ORIGINS = [ 
        "http://"+APP_DOMAIN,
        "https://"+APP_DOMAIN
    ]

    PG_USER = values.Value("admin")
    PG_PASSWORD = values.Value("admin")
    PG_DOMAIN = values.Value("postgres")
    PG_PORT = values.IntegerValue(5432)
    PG_DB_NAME = values.Value("postgres")
    DATABASES = values.DatabaseURLValue(
        f"postgres://{PG_USER}:{PG_PASSWORD}@{PG_DOMAIN}:{PG_PORT}?{PG_DB_NAME}"
    )
    
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
                "class": "logging.StreamHandler",
                "stream": "/var/log/balance_app.log",
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