# vim:set sw=4 ts=4 et:

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect 
from django import forms
from django.db import models
from django_quicky import routing, view

from vaper.models import Flavour, Manufacturer

url, urlpatterns = routing()

@login_required
def view(request, id):
    flavour = get_object_or_404(Flavour, id=id)
    recipes = set([ r.recipes for r in flavour.flavour_instances.all() ])
    
    return render(request, 'vaper/flavour/view.html', {
        'flavour': flavour,
        'recipes': recipes,
    })

@url('^(?P<id>[0-9]+)/edit/$', name='ui/flavour/edit')
@permission_required('vaper.change_flavour')
def edit(request, id):
    flavour = get_object_or_404(Flavour, id=id)
    return render(request, 'vaper/dialog/flavour/edit.html', {
        'flavour': flavour,
    })

@url('^add/$', name='ui/flavour/add')
@permission_required('vaper.add_flavour')
def add(request):
    return render(request, 'vaper/dialog/flavour/edit.html', {
        'flavour': {
            'name': '',
            'manufacturer': '',
            'ml': 10,
        },
    })
