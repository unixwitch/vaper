# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-18 23:22
from __future__ import unicode_literals

from django.db import migrations, models

def set_ml(apps, schema_editor):
    Flavour = apps.get_model("vaper", "Flavour")
    for flavour in Flavour.objects.all():
        flavour.ml = flavour.ml_remaining
        flavour.save()

class Migration(migrations.Migration):

    dependencies = [
        ('vaper', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='flavour',
            name='ml',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7, verbose_name=b'Remaining (ml)'),
            preserve_default=False,
        ),
        migrations.RunPython(set_ml),
    ]
