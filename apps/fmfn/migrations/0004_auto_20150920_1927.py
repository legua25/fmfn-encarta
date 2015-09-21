# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fmfn', '0003_auto_20150920_1926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='class_grades',
            field=models.ManyToManyField(related_name='+', verbose_name='class grades', to='fmfn.Grade'),
        ),
    ]
