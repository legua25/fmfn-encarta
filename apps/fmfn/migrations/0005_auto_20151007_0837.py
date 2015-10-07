# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fmfn', '0004_auto_20151006_1836'),
    ]

    operations = [
        migrations.RenameField(
            model_name='campus',
            old_name='mane',
            new_name='name',
        ),
        migrations.AlterField(
            model_name='user',
            name='father_family_name',
            field=models.CharField(default='', max_length=64, verbose_name="father's family name", blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='mother_family_name',
            field=models.CharField(default='', max_length=64, verbose_name="mother's family name", blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.ForeignKey(related_name='members', default=1, verbose_name='user role', to='fmfn.Role'),
        ),
    ]
