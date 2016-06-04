# vim:set sw=4 ts=4 et:

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect 
from django import forms
from django.db import models
from vaper.models import Recipe

@permission_required('vaper.change_recipe')
def edit(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    return render(request, 'vaper/dialog/recipe/edit.html', {
        'recipe': recipe,
    })

@permission_required('vaper.add_recipe')
def add(request):
    return render(request, 'vaper/dialog/recipe/edit.html', {
        'recipe': {
            'name': '',
            'description': '',
        },
    })
