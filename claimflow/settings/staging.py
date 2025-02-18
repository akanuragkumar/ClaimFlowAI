from .base import *
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

env_data = get_secret('staging')

db_name = env_data.get('DATABASE_SECRETS').get('NAME')

if env_data.get('DATABASE_SECRETS').get('ENGINE') == "django.db.backends.sqlite3":
    db_name = str(BASE_DIR / db_name)

DATABASES = {
    'default': {
        'ENGINE': env_data.get('DATABASE_SECRETS').get('ENGINE'),
        'NAME': db_name
    }
}

DEBUG = env_data.get('DEBUG')
