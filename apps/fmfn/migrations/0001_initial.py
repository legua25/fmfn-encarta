# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64, verbose_name='type name')),
                ('description', models.CharField(max_length=256, verbose_name='type description')),
            ],
            options={
                'verbose_name': 'material language',
                'verbose_name_plural': 'material languages',
            },
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128)),
                ('description', models.CharField(max_length=1024, verbose_name='material description')),
                ('suggested_agee', models.PositiveSmallIntegerField(choices=[(1, 'kindergarten'), (2, 'pre school'), (3, 'low elementary school'), (4, 'high elementary school'), (5, 'junior high school')])),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'material',
                'verbose_name_plural': 'materials',
            },
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64, verbose_name='type name')),
                ('description', models.CharField(max_length=256, verbose_name='type description')),
                ('materials', models.ForeignKey(related_name='themes', verbose_name='tagged materials', to='fmfn.Material')),
            ],
            options={
                'verbose_name': 'material type',
                'verbose_name_plural': 'material types',
            },
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64, verbose_name='type name')),
                ('description', models.CharField(max_length=256, verbose_name='type description')),
                ('materials', models.ForeignKey(related_name='types', verbose_name='tagged materials', to='fmfn.Material')),
            ],
            options={
                'verbose_name': 'material type',
                'verbose_name_plural': 'material types',
            },
        ),
        migrations.AddField(
            model_name='language',
            name='materials',
            field=models.ForeignKey(related_name='languages', verbose_name='tagged materials', to='fmfn.Material'),
        ),
    ]
