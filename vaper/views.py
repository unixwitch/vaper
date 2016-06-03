# vim:sw=4 ts=4 et:

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
import models

@login_required
def index(request):
    flavours = models.Flavour.objects.all()
    recipes  = models.Recipe.objects.all()

    return render(request, 'vaper/index.html', {
        'recipes': recipes,
        'flavours': flavours,
    })

@login_required
def flavour(request, id):
    flavour = get_object_or_404(models.Flavour, id=id)
    recipes = set([ r.recipes for r in flavour.flavour_instances.all() ])
    
    return render(request, 'vaper/flavour.html', {
        'flavour': flavour,
        'recipes': recipes,
    })

@login_required
def recipe(request, id):
    recipe = get_object_or_404(models.Recipe, id=id)
    
    return render(request, 'vaper/recipe.html', {
        'recipe': recipe,
    })
