from .base import *

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
if env('IS_GITHUB_WORKFLOW') == "no":
    print("local")
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'postgres',
            'USER': 'postgres',
            'PASSWORD': 'postgres',
            'HOST': 'db',
            'PORT': 5432,
        }
    }