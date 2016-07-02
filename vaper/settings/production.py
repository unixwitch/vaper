# vim:sw=4 ts=4 et:
from .base import *

ALLOWED_HOSTS = [ 'vaper.le-fay.org' ]

ADMINS = (
    ( 'Felicity Tarnell', 'ft@le-fay.org' ),
)

try:
    from .local import *
except ImportError:
    pass
