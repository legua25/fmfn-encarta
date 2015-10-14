# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import apps.fmfn.models.users
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('fmfn', '0002_auto_20151011_1248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=imagekit.models.fields.ProcessedImageField(default='users/default.png', upload_to=apps.fmfn.models.users.upload_photo, verbose_name='user photo', blank=True),
        ),
    ]
