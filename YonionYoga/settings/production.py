from .base import *

DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^pbj9p#)l1k5p5&0lvn+07*kxk#@cd&=%mx+u2-j!@kqf4mmo0'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['192.168.31.183', '127.0.0.1']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

try:
    from .local import *
except ImportError:
    pass
