import json
import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


def get_secret(setting):
    file_path = str(str(BASE_DIR) + '/settings/secrets.json')
    try:
        with open(file_path) as file:
            secrets = json.loads(file.read())
            try:
                return secrets[setting]
            except KeyError:
                error_message = "Set the {0} environment variable".format(setting)
                raise ImproperlyConfigured(error_message)
    except FileNotFoundError:
        error_message = "secrets.json not found in settings folder"
        raise ImproperlyConfigured(error_message)


DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
THIRD_PARTY_APPS = [
    'rest_framework',
    'django_fsm_log',
    'django_filters',
    'django_fsm',
]
WAAS_APPS = [
    'tenant',
    'loss_run',
    'base',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + WAAS_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
]
ROOT_URLCONF = 'claimflow.urls'

env_data = get_secret('base')

SECRET_KEY = env_data.get('SECRET_KEY')

ALLOWED_HOSTS = ['*']

WSGI_APPLICATION = env_data.get('WSGI_APPLICATION')

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), "/src/static")

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 2,
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
}

CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"

OPENAI_API_KEY = env_data.get('OPENAI_API_KEY')
