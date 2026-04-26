from .base import *
import dj_database_url
import os
from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

load_dotenv()

DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv('ALLOWED_HOSTS', '*').split(',')
    if host.strip()
]

CORS_ALLOW_ALL_ORIGINS = True

# postgresql manzili
database_url = os.getenv('DATABASE_URL')
if database_url:
    DATABASES = {
        'default': dj_database_url.parse(
            database_url,
            conn_max_age=0,
            ssl_require=True,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# middleware sozlamasi
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')


# storage sozlamasi 
imagekit_public_key = os.getenv('IMAGEKIT_PUBLIC_KEY')
imagekit_private_key = os.getenv('IMAGEKIT_PRIVATE_KEY')
imagekit_url_endpoint = os.getenv('IMAGEKIT_URL_ENDPOINT')

if imagekit_public_key and imagekit_private_key and imagekit_url_endpoint:
    INSTALLED_APPS += ['imagekitio_storage']

    # SDK 'IMAGEKIT_STORAGE' kalitini o'qiydi (IMAGEKITIO_SETTINGS emas)
    IMAGEKIT_STORAGE = {
        'PUBLIC_KEY': imagekit_public_key,
        'PRIVATE_KEY': imagekit_private_key,
        'URL_ENDPOINT': imagekit_url_endpoint,
    }

    STORAGES = {
        "default": {
            "BACKEND": "common.storage.PatchedMediaImagekitStorage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }
else:
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }