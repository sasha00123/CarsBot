from .base import *

DEBUG = False

DATABASES = {
    'default': dj_database_url.config()
}
SEND_FILE = "LINK"
