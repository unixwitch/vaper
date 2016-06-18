# vim:sw=4 ts=4 et:

from django import forms
from django.db import models, IntegrityError
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from django_quicky import routing, view
from django.core.urlresolvers import reverse
from vaper.models import Flavour, Manufacturer
import json

url, urlpatterns = routing()

class FlavourForm(forms.ModelForm):
    manuf = forms.CharField(max_length=64)

    class Meta:
        model = Flavour
        fields = [
            'name',
            'ml_remaining',
        ]

@url('^edit/$', name='api/flavour/edit')
@login_required
@require_http_methods(['POST'])
@view(render_to='json')
def edit(request):
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

    return {
        'status': 'success',
        'message': 'Flavour added successfully',
    }

@url('^autocomplete/$', name='api/flavour/autocomplete')
@login_required
@require_http_methods(['GET'])
@view(render_to='json')
def autocomplete(request):
    flavours = Flavour.objects.filter(name__icontains=request.GET['query'])

    suggestions = [
        {
            "value": "{} ({})".format(f.name, f.manufacturer),
            "data": f.id,
        } for f in flavours
    ]

    return {
        'query': request.GET['query'],
        'suggestions': suggestions,
    }
