# vim:sw=4 ts=4 et:
from .base import *

ALLOWED_HOSTS = [ 'vaper.le-fay.org' ]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'vaper',
    }
}

ADMINS = (
    ( 'Felicity Tarnell', 'ft@le-fay.org' ),
)

COMPRESS_OFFLINE = True

try:
    from .local import *
except ImportError:
    pass
