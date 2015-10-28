# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fmfn', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='download',
            name='material',
            field=models.ForeignKey(related_name='+', verbose_name='material', to='fmfn.Material'),
        ),
    ]
