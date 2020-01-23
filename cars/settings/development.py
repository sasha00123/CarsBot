from .base import *

DEBUG = True

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.spatialite',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# MAIL
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
