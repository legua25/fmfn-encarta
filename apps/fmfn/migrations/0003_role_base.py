# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fmfn', '0002_auto_20151006_1820'),
    ]

    operations = [
        migrations.AddField(
            model_name='role',
            name='base',
            field=models.ForeignKey(related_name='subroles', default=1, verbose_name='base role', to='fmfn.Role'),
            preserve_default=False,
        ),
    ]
