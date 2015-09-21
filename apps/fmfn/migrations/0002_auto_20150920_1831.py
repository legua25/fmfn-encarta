# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fmfn', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True, verbose_name='is active')),
            ],
            options={
                'verbose_name': 'portfolio',
                'verbose_name_plural': 'portfolios',
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True, verbose_name='is active')),
                ('description', models.CharField(max_length=64, verbose_name='description')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
            ],
            options={
                'verbose_name': 'material report',
                'verbose_name_plural': 'material reports',
            },
        ),
        migrations.RemoveField(
            model_name='material',
            name='suggested_agee',
        ),
        migrations.AddField(
            model_name='language',
            name='active',
            field=models.BooleanField(default=True, verbose_name='is active'),
        ),
        migrations.AddField(
            model_name='material',
            name='suggested_ages',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='suggested ages', choices=[(1, 'kindergarten'), (2, 'pre school'), (3, 'low elementary school'), (4, 'high elementary school'), (5, 'junior high school')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='theme',
            name='active',
            field=models.BooleanField(default=True, verbose_name='is active'),
        ),
        migrations.AddField(
            model_name='type',
            name='active',
            field=models.BooleanField(default=True, verbose_name='is active'),
        ),
        migrations.AlterField(
            model_name='material',
            name='description',
            field=models.CharField(max_length=1024, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='material',
            name='user',
            field=models.ForeignKey(related_name='materials', verbose_name='uploading user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='report',
            name='material',
            field=models.ForeignKey(related_name='+', verbose_name='reported material', to='fmfn.Material'),
        ),
        migrations.AddField(
            model_name='report',
            name='user',
            field=models.ForeignKey(related_name='reports', verbose_name='reporting author', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='materials',
            field=models.ManyToManyField(related_name='+', verbose_name='materials', to='fmfn.Material'),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='user',
            field=models.ForeignKey(related_name='portfolio', verbose_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]
