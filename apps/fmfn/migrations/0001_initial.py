# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import apps.fmfn.models.users
from django.conf import settings
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('active', models.BooleanField(default=True, verbose_name='is active')),
                ('email_address', models.EmailField(unique=True, max_length=255, verbose_name='email address')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('first_name', models.CharField(max_length=64, verbose_name='first name')),
                ('father_family_name', models.CharField(default='', max_length=64, verbose_name="father's family name", blank=True)),
                ('mother_family_name', models.CharField(default='', max_length=64, verbose_name="mother's family name", blank=True)),
                ('photo', imagekit.models.fields.ProcessedImageField(default='users/default.jpg', upload_to=apps.fmfn.models.users.upload_photo, verbose_name='user photo', blank=True)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
        ),
        migrations.CreateModel(
            name='ActionLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True, verbose_name='is active')),
                ('category', models.PositiveSmallIntegerField(verbose_name='performed action category', choices=[(1, 'account control'), (2, 'content management'), (4, 'tag management')])),
                ('action', models.CharField(max_length=512, verbose_name='performed action', db_index=True)),
                ('status', models.PositiveSmallIntegerField(verbose_name='performed action status code')),
                ('action_date', models.DateTimeField(auto_now_add=True, verbose_name='performed action date', db_index=True)),
                ('user', models.ForeignKey(related_name='+', verbose_name='user', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'action log',
                'verbose_name_plural': 'action logs',
            },
        ),
        migrations.CreateModel(
            name='Campus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True, verbose_name='is active')),
                ('name', models.CharField(max_length=256, verbose_name='campus name')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='date added')),
            ],
            options={
                'verbose_name': 'campus',
                'verbose_name_plural': 'campi',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True, verbose_name='is active')),
                ('content', models.CharField(max_length=500, verbose_name='comment content')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('rating_value', models.PositiveSmallIntegerField(verbose_name='rating values', choices=[(1, 'bad'), (2, 'regular'), (3, 'good'), (4, 'very good'), (5, 'excellent')])),
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
            ],
            options={
                'verbose_name': 'download',
                'verbose_name_plural': 'downloads',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True, verbose_name='is active')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='date added')),
            ],
            options={
                'verbose_name': 'portfolio item',
                'verbose_name_plural': 'portfolio items',
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True, verbose_name='is active')),
                ('name', models.CharField(max_length=64, verbose_name='type name')),
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
                ('title', models.CharField(max_length=128, verbose_name='title')),
                ('content', models.FileField(upload_to='materials/files', null=True, verbose_name='content file', blank=True)),
                ('link', models.URLField(null=True, verbose_name='content link', blank=True)),
                ('description', models.CharField(max_length=1024, null=True, verbose_name='description', blank=True)),
                ('languages', models.ManyToManyField(related_name='materials', verbose_name='material language', to='fmfn.Language', blank=True)),
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
                ('user', models.ForeignKey(related_name='portfolio', verbose_name='user', to=settings.AUTH_USER_MODEL)),
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
                ('status', models.PositiveSmallIntegerField(default=1, blank=True, verbose_name='report status', choices=[(1, 'in progress'), (2, 'resolved'), (4, 'rejected')])),
                ('material', models.ForeignKey(related_name='+', verbose_name='reported material', to='fmfn.Material')),
                ('user', models.ForeignKey(related_name='reports', verbose_name='reporting author', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'material report',
                'verbose_name_plural': 'material reports',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True, verbose_name='is active')),
                ('name', models.CharField(max_length=64, verbose_name='role name')),
                ('description', models.CharField(default='', max_length=512, verbose_name='role description')),
                ('base', models.ForeignKey(related_name='subroles', verbose_name='base role', to='fmfn.Role', null=True)),
                ('base_permissions', models.ManyToManyField(related_query_name='role', related_name='roles', verbose_name='permissions', to='auth.Permission')),
            ],
            options={
                'verbose_name': 'user role',
                'verbose_name_plural': 'user roles',
            },
        ),
        migrations.CreateModel(
            name='SchoolGrade',
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
            name='Theme',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True, verbose_name='is active')),
                ('name', models.CharField(max_length=64, verbose_name='type name')),
            ],
            options={
                'verbose_name': 'material theme',
                'verbose_name_plural': 'material themes',
            },
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True, verbose_name='is active')),
                ('name', models.CharField(max_length=64, verbose_name='type name')),
            ],
            options={
                'verbose_name': 'material type',
                'verbose_name_plural': 'material types',
            },
        ),
        migrations.AddField(
            model_name='material',
            name='suggested_ages',
            field=models.ManyToManyField(related_name='materials', verbose_name='suggested ages', to='fmfn.SchoolGrade', blank=True),
        ),
        migrations.AddField(
            model_name='material',
            name='themes',
            field=models.ManyToManyField(related_name='materials', verbose_name='material theme', to='fmfn.Theme', blank=True),
        ),
        migrations.AddField(
            model_name='material',
            name='types',
            field=models.ManyToManyField(related_name='materials', verbose_name='material type', to='fmfn.Type', blank=True),
        ),
        migrations.AddField(
            model_name='material',
            name='user',
            field=models.ForeignKey(related_name='materials', verbose_name='uploading user', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='material',
            field=models.ForeignKey(related_name='+', verbose_name='material', to='fmfn.Material'),
        ),
        migrations.AddField(
            model_name='item',
            name='portfolio',
            field=models.ForeignKey(related_name='items', verbose_name='portfolio items', to='fmfn.Portfolio'),
        ),
        migrations.AddField(
            model_name='download',
            name='material',
            field=models.ForeignKey(related_name='+', verbose_name='material', to='fmfn.Material'),
        ),
        migrations.AddField(
            model_name='download',
            name='user',
            field=models.ForeignKey(related_name='+', verbose_name='user', to=settings.AUTH_USER_MODEL),
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
            model_name='user',
            name='campus',
            field=models.ForeignKey(related_name='users', default=None, verbose_name='campus', to='fmfn.Campus', null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='grades',
            field=models.ManyToManyField(related_name='users', verbose_name='school grades', to='fmfn.SchoolGrade'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.ForeignKey(related_name='members', default=None, verbose_name='user role', to='fmfn.Role', null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions'),
        ),
    ]
