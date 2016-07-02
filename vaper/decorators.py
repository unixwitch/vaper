# vim:sw=4 ts=4 et:

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test

def superuser_required(view_func=None, redirect_field_name=REDIRECT_FIELD_NAME,
                       login_url='vaper:user/login'):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_superuser,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator

def staff_required(view_func=None, redirect_field_name=REDIRECT_FIELD_NAME,
                   login_url='vaper:user/login'):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_staff,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator
