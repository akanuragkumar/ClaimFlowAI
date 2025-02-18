from .base import *

env_data = get_secret('prod')

DATABASES = {
    'default': {
        'ENGINE': env_data.get('DATABASE_SECRETS').get('ENGINE'),
        'NAME': env_data.get('DATABASE_SECRETS').get('NAME'),
        'USER': env_data.get('DATABASE_SECRETS').get('USER'),
        'PASSWORD': env_data.get('DATABASE_SECRETS').get('PASSWORD'),
        'HOST': env_data.get('DATABASE_SECRETS').get('HOST'),
        'PORT': env_data.get('DATABASE_SECRETS').get('PORT'),
    }
}

DEBUG = env_data.get('DEBUG')