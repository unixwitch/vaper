# vim:sw=4 ts=4 et:

from django_quicky import routing, view
from vaper.decorators import superuser_required

url, urlpatterns = routing()

@url('^list/', name='admin/user/list')
@superuser_required
def list(request):
    pass
