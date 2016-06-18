# vim:set sw=4 ts=4 et:

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect 
from django import forms
from django.db import models
from django_quicky import routing, view
from vaper.models import Recipe

url, urlpatterns = routing()

@url(r'^ui/recipe/(?P<id>[0-9]+)/edit/$', name='ui/recipe/edit')
@permission_required('vaper.change_recipe')
def edit(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    return render(request, 'vaper/dialog/recipe/edit.html', {
        'recipe': recipe,
    })

@url(r'^ui/recipe/add/$', name='ui/recipe/add')
@permission_required('vaper.add_recipe')
def add(request):
    return render(request, 'vaper/dialog/recipe/edit.html', {
        'recipe': {
            'name': '',
            'description': '',
            'flavour_instances': [],
        },
    })

@url(r'^ui/recipe/(?P<id>[0-9]+)/delete/$', name='ui/recipe/delete')
@permission_required('vaper.delete_recipe')
def delete(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    return render(request, 'vaper/dialog/recipe/delete.html', {
        'recipe': recipe,
    })
