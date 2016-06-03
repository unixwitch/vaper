from .base import *

ALLOWED_HOSTS = [ 'vaper.le-fay.org' ]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'vaper',
    }
}

try:
    from .local import *
except ImportError:
    pass
