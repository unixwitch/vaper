# vim:sw=4 ts=4 et:

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from vaper.models import Manufacturer
import json

@login_required
def autocomplete(request):
    return HttpResponse(
        json.dumps({
            'query': request.GET['query'],
            'suggestions': [
                m.name for m in Manufacturer.objects.filter(name__icontains=request.GET['query'])
            ],
        }),
        content_type='text/plain')
