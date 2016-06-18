# vim:sw=4 ts=4 et:

from django import forms
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from vaper.models import Recipe, Flavour, FlavourInstance
from django_quicky import routing, view
from django.shortcuts import get_object_or_404
import json

url, urlpatterns = routing()

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            'name',
            'description',
        ]

@url('^edit/$', name='api/recipe/edit')
@login_required
@require_http_methods(['POST'])
@view(render_to='json')
def edit(request):
    data = json.loads(request.POST['data'])
    print data

    if 'id' in data:
        recipe = get_object_or_404(Recipe, id=data['id'])
        form = RecipeForm(data, instance=recipe)
    else:
        form = RecipeForm(data)

    if not form.is_valid():
        return JsonResponse({
            'status': 'error',
            'errors':  form.errors,
        }, status=400)

    numflavours = int(data['numflavours'])

    errors = {}

    for fn in range(0, numflavours):
        flavour_id = data['flavour_{}_name_data'.format(fn)]

        if flavour_id == '':
            errors['flavour-{}'.format(fn)] = 'Flavour not found in database'

    if len(errors) > 0:
        return JsonResponse({
            'status': 'error',
            'errors': errors,
        }, status=400)

    recipe = form.instance
    recipe.flavour_instances.all().delete()
    form.save()

    for fn in range(0, numflavours):
        flavour_id = data['flavour_{}_name_data'.format(fn)]
        flavour_strength = data['flavour_{}_strength'.format(fn)]

        flavour = Flavour.objects.get(id=flavour_id)

        recipe.flavour_instances.create(
            flavour = flavour,
            strength = flavour_strength,
        )

    recipe.save()

    return {
        'status': 'success',
        'message': 'Recipe added successfully',
    }
