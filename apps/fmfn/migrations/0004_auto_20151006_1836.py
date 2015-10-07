# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fmfn', '0003_role_base'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='base',
            field=models.ForeignKey(related_name='subroles', verbose_name='base role', to='fmfn.Role', null=True),
        ),
    ]
