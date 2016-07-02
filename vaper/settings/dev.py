from .base import *

DEBUG = True

SECRET_KEY = 'change this in production'

#MIDDLEWARE_CLASSES += (
#    'django_quicky.middleware.ForceSuperUserMiddleWare',
#)

try:
    from .local import *
except ImportError:
    pass
