# vim:set sw=4 ts=4 et:

from django.utils.safestring import mark_safe
from django.template import Library

import simplejson

register = Library()

@register.filter(is_safe=True)
def js(obj):
    return mark_safe(simplejson.dumps(obj))
