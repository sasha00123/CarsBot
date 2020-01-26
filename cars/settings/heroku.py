from .base import *

MIDDLEWARE = ['whitenoise.middleware.WhiteNoiseMiddleware',] + MIDDLEWARE
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

