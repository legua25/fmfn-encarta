# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fmfn', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='role',
            name='members',
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.ForeignKey(related_name='members', default=1, verbose_name='user role', to='fmfn.Role'),
            preserve_default=False,
        ),
    ]
