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
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True, verbose_name='is active')),
                ('content', models.CharField(max_length=64, verbose_name='comment content')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
            ],
            options={
                'verbose_name': 'material comment',
                'verbose_name_plural': 'material comments',
            },
        ),
        migrations.CreateModel(
            name='Download',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True, verbose_name='is active')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='date')),
                ('material', models.ForeignKey(related_name='+', verbose_name='material', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(related_name='+', verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'download',
                'verbose_name_plural': 'downloads',
            },
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True, verbose_name='is active')),
                ('name', models.CharField(max_length=64, verbose_name='name')),
                ('min_age', models.PositiveSmallIntegerField(verbose_name='minimum expected age')),
                ('max_age', models.PositiveSmallIntegerField(verbose_name='maximum expected age')),
            ],
            options={
                'verbose_name': 'school grade',
                'verbose_name_plural': 'school grades',
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True, verbose_name='is active')),
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
                ('active', models.BooleanField(default=True, verbose_name='is active')),
                ('title', models.CharField(max_length=128)),
                ('description', models.CharField(max_length=1024, verbose_name='description')),
                ('suggested_ages', models.ManyToManyField(related_name='materials', verbose_name='suggested ages', to='fmfn.Grade')),
                ('user', models.ForeignKey(related_name='materials', verbose_name='uploading user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'material',
                'verbose_name_plural': 'materials',
            },
        ),
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True, verbose_name='is active')),
                ('materials', models.ManyToManyField(related_name='+', verbose_name='materials', to='fmfn.Material')),
                ('user', models.ForeignKey(related_name='portfolio', verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'portfolio',
                'verbose_name_plural': 'portfolios',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True, verbose_name='is active')),
                ('campus', models.CharField(max_length=64, null=True, verbose_name='campus')),
                ('class_grades', models.ManyToManyField(related_name='+', verbose_name='class grades', to='fmfn.Grade')),
                ('user', models.ForeignKey(related_name='profile', verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'user profile',
                'verbose_name_plural': 'user profiles',
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True, verbose_name='is active')),
                ('rating_value', models.PositiveSmallIntegerField(verbose_name='rating values', choices=[(1, 'bad'), (2, 'regular'), (3, 'good'), (4, 'very good'), (5, 'excellent')])),
                ('material', models.ForeignKey(related_name='ratings', verbose_name='material', to='fmfn.Material')),
                ('user', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'rating',
                'verbose_name_plural': 'ratings',
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True, verbose_name='is active')),
                ('description', models.CharField(max_length=64, verbose_name='description')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('material', models.ForeignKey(related_name='+', verbose_name='reported material', to='fmfn.Material')),
                ('user', models.ForeignKey(related_name='reports', verbose_name='reporting author', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'material report',
                'verbose_name_plural': 'material reports',
            },
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True, verbose_name='is active')),
                ('name', models.CharField(max_length=64, verbose_name='type name')),
                ('description', models.CharField(max_length=256, verbose_name='type description')),
                ('materials', models.ManyToManyField(related_name='themes', verbose_name='tagged materials', to='fmfn.Material')),
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
                ('active', models.BooleanField(default=True, verbose_name='is active')),
                ('name', models.CharField(max_length=64, verbose_name='type name')),
                ('description', models.CharField(max_length=256, verbose_name='type description')),
                ('materials', models.ManyToManyField(related_name='types', verbose_name='tagged materials', to='fmfn.Material')),
            ],
            options={
                'verbose_name': 'material type',
                'verbose_name_plural': 'material types',
            },
        ),
        migrations.AddField(
            model_name='language',
            name='materials',
            field=models.ManyToManyField(related_name='languages', verbose_name='tagged materials', to='fmfn.Material'),
        ),
        migrations.AddField(
            model_name='comment',
            name='material',
            field=models.ForeignKey(related_name='comments', verbose_name='commented material', to='fmfn.Material'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(related_name='comments', verbose_name='author', to=settings.AUTH_USER_MODEL),
        ),
    ]
