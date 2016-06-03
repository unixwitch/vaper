from .base import *

DEBUG = True

SECRET_KEY = 'change this in production'

try:
    from .local import *
except ImportError:
    pass
