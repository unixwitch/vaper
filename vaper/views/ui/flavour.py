# vim:set sw=4 ts=4 et:

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect 
from django import forms
from django.db import models
from vaper.models import Flavour, Manufacturer

@login_required
def view(request, id):
    flavour = get_object_or_404(Flavour, id=id)
    recipes = set([ r.recipes for r in flavour.flavour_instances.all() ])
    
    return render(request, 'vaper/flavour/view.html', {
        'flavour': flavour,
        'recipes': recipes,
    })

@permission_required('vaper.change_flavour')
def edit(request, id):
    flavour = get_object_or_404(Flavour, id=id)
    return render(request, 'vaper/dialog/flavour/edit.html', {
        'flavour': flavour,
    })

@permission_required('vaper.add_flavour')
def add(request):
    return render(request, 'vaper/dialog/flavour/edit.html', {
        'flavour': {
            'name': '',
            'manufacturer': '',
            'ml': 10,
        },
    })

#@login_required
#def delete(request, id):
#    pass
