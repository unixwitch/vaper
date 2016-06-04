# vim:sw=4 ts=4 et:

from django import forms
from django.http import JsonResponse
from vaper.models import Recipe

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            'name',
            'description',
        ]

def edit(request):
    if request.method != 'POST':
        return JsonResponse({
            'status': 'error',
            'errors': [ 'Invalid method' ],
        }, status=400)

    data = json.loads(request.POST['data'])
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

    form.save()

    return JsonResponse({
        'status': 'success',
        'message': 'Recipe added successfully',
    })
