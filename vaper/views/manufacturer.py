# vim:sw=4 ts=4 et:

from django_quicky import routing, view
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404
from vaper.models import Manufacturer, Flavour

url, urlpatterns = routing()

@url('^(?P<id>[0-9]+)/edit/$', name='manufacturer/edit')
@permission_required('vaper.change_manufacturer')
def edit(request, id):
    pass

@url('^(?P<id>[0-9]+)/$', name='manufacturer/view')
@login_required
def view(request, id):
    manufacturer = get_object_or_404(Manufacturer, id=id)
    flavours = manufacturer.flavours.all()

    return render(request, 'vaper/manufacturer/view.html', {
        'manufacturer': manufacturer,
        'flavours': flavours,
    })
