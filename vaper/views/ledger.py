
from django import forms
from django_quicky import routing, view
from django.shortcuts import render, redirect, get_object_or_404
from datetimewidget.widgets import DateWidget
from vaper import models
from vaper.decorators import staff_required
import datetime

url, urlpatterns = routing()

@url('^$', name='ledger')
@staff_required
def index(request):
    entries = models.LedgerEntry.objects.all().order_by('-date', '-id')
    ledger = models.Ledger.load()
    return render(request, 'vaper/ledger/index.html', {
        'ledger': ledger,
        'entries': entries,
    })

class AddLedgerForm(forms.ModelForm):
    class Meta:
        model = models.LedgerEntry
        fields = [
            'date',
            'description',
            'amount',
        ]
        widgets = {
            'date': DateWidget(
                        bootstrap_version=3,
                        attrs = {
                            'id': 'datewidget',
                        },
                        options = {
                            'format': 'yyyy-mm-dd',
                            'todayBtn': 'true',
                            'todayHighlight': 'true',
                        }
                    ),
        }

@url('add/$', name='ledger/add')
@staff_required
def add(request):
    if request.method == 'POST':
        form = AddLedgerForm(request.POST)
        if form.is_valid():
            ledger = models.Ledger.load()
            form.instance.ledger = ledger
            ledger.balance += form.instance.amount
            form.save()
            ledger.save()
            return redirect('vaper:ledger')
    else:
        form = AddLedgerForm(initial = { 'date': datetime.date.today() })

    return render(request, 'vaper/ledger/add.html', {
        'form': form,
    })
