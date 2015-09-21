# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fmfn', '0002_auto_20150920_1831'),
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
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True, verbose_name='is active')),
                ('class_grades', models.ManyToManyField(related_name='+', null=True, verbose_name='class grades', to='fmfn.Grade')),
                ('user', models.ForeignKey(related_name='profile', verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True, verbose_name='is active')),
                ('rating_value', models.PositiveSmallIntegerField(verbose_name='rating values', choices=[(1, 'bad'), (2, 'regular'), (3, 'good'), (4, 'very good'), (5, 'excellent')])),
            ],
            options={
                'verbose_name': 'rating',
                'verbose_name_plural': 'ratings',
            },
        ),
        migrations.RemoveField(
            model_name='material',
            name='suggested_ages',
        ),
        migrations.AddField(
            model_name='material',
            name='active',
            field=models.BooleanField(default=True, verbose_name='is active'),
        ),
        migrations.AddField(
            model_name='rating',
            name='material',
            field=models.ForeignKey(related_name='ratings', verbose_name='material', to='fmfn.Material'),
        ),
        migrations.AddField(
            model_name='rating',
            name='user',
            field=models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL),
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
        migrations.AddField(
            model_name='material',
            name='suggested_grades',
            field=models.ManyToManyField(related_name='ages', verbose_name='suggested grade', to='fmfn.Grade'),
        ),
    ]
