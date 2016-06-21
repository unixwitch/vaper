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

class FlavourForm(forms.ModelForm):
    manuf = forms.CharField(max_length=64)

    class Meta:
        model = Flavour
        fields = [
            'name',
            'ml',
        ]

@permission_required('vaper.change_flavour')
def edit(request, id):
    flavour = get_object_or_404(Flavour, id=id)

    if request.method == 'POST':
        form = FlavourForm(
                request.POST,
                instance = flavour)

        if form.is_valid():
            manufacturer, created = Manufacturer.objects.get_or_create(name=form.cleaned_data['manuf'])
            form.instance.manufacturer = manufacturer
            form.save()
            return HttpResponseRedirect(reverse('vaper:flavour/view', args=[form.instance.id]))
    else:
        form = FlavourForm(instance=flavour)

    return render(request, 'vaper/flavour/edit.html', {
        'flavour': flavour,
        'form':    form,
    })

@permission_required('vaper.delete_flavour')
def delete(request, id):
    pass
