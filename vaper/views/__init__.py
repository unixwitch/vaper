# vim:sw=4 ts=4 et:

from decimal import Decimal
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
import json
from vaper import models

@login_required
def index(request):
    manufacturers = models.Manufacturer.objects.all().order_by('name')
    recipes  = models.Recipe.objects.all().order_by('name')

    flavours_by_manuf = [ ( manuf, manuf.flavours.all().order_by('name') ) for manuf in manufacturers ]
    #flavours_by_manuf = {}
    #for manuf in manufacturers:
    #    flavours_by_manuf[manuf.name] = manuf.flavours.all().order_by('name')
    #print flavours_by_manuf

    return render(request, 'vaper/index.html', {
        'recipes': recipes,
        'manufacturers': manufacturers,
        'flavours_by_manuf': flavours_by_manuf
    })

@login_required
def recipe(request, id):
    recipe = get_object_or_404(models.Recipe, id=id)
    
    return render(request, 'vaper/recipe.html', {
        'recipe': recipe,
    })

@login_required
def stock(request):
    return render(request, 'vaper/stock.html', {
        'stock': models.Flavour.objects.all().order_by('ml')
    })

@login_required
def api_stock_mix(request):
    data = json.loads(request.POST['stock'])

    for flavour in data:
        o = models.Flavour.objects.get(id=flavour['id'])
        o.ml -= Decimal(flavour['ml'])
        o.save()

    return HttpResponse("okay", content_type='text/plain')
