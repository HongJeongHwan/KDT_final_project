from .base import *

ALLOWED_HOSTS = ['52.79.44.164']
STATIC_ROOT = BASE_DIR / 'static/'
STATICFILES_DIRS = []
DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pybo',
        'USER': 'dbmasteruser',
        'PASSWORD': 'votmdnjem1234',
        'HOST': 'ls-899b0b24494e190f9d6363bf5503b0b30395fb2a.c3ms6ca44pmh.ap-northeast-2.rds.amazonaws.com',
        'PORT': '5432',
    }
}