# vim:sw=4 ts=4 et:

from django import forms
from django.db import models, IntegrityError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from vaper.models import Flavour, Manufacturer
import json

class FlavourForm(forms.ModelForm):
    manuf = forms.CharField(max_length=64)

    class Meta:
        model = Flavour
        fields = [
            'name',
            'ml_remaining',
        ]

def edit(request):
    if request.method != 'POST':
        return JsonResponse({
            'status': 'error',
            'errors': [ 'Invalid method' ],
        }, status=400)

    data = json.loads(request.POST['data'])
    if 'id' in data:
        flavour = get_object_or_404(Flavour, id=data['id'])
        form = FlavourForm(data, instance=flavour)
    else:
        form = FlavourForm(data)

    if not form.is_valid():
        return JsonResponse({
            'status': 'error',
            'errors':  form.errors,
        }, status=400)

    manufacturer, created = Manufacturer.objects.get_or_create(name=form.cleaned_data['manuf'])
    form.instance.manufacturer = manufacturer

    try:
        form.save()
    except IntegrityError:
        return JsonResponse({
            'status': 'error',
            'errors': {
                'name': [ 'This flavour/manufacturer combination already exists', ],
            },
        }, status=400)

    return JsonResponse({
        'status': 'success',
        'message': 'Flavour added successfully',
    })
