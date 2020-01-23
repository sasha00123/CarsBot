from .base import *

DEBUG = False

DATABASES = {
    'default': dj_database_url.config()
}

MIDDLEWARE = ['whitenoise.middleware.WhiteNoiseMiddleware',] + MIDDLEWARE
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

