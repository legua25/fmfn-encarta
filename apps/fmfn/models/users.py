# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import (
	AbstractBaseUser,
	Permission,
	BaseUserManager,
	PermissionsMixin
)
from django.utils.translation import ugettext_lazy as _
from django.utils.functional import cached_property
from imagekit.processors import ResizeToFill
from django.utils.timezone import now
from django.conf import settings
from django.db.models import *
from imagekit.models.fields import ProcessedImageField as ImageField
from _base import Model, ActiveManager

class UserManager(ActiveManager, BaseUserManager):

	def _create(self, email_address = None, password = None, **kwargs):

		if email_address is None: raise ValueError('Email address cannot be null')

		email = UserManager.normalize_email(email_address)
		user = self.model(
			email_address = email,
			date_joined = now(),
			**kwargs
		)

		user.set_password(password)
		user.save()

		return user
	def create_user(self, email_address, password = None, **extra_fields):
		return self._create(email_address, password, **extra_fields)
	def create_superuser(self, email_address, password, **extra_fields):
		return  self._create(email_address, password, is_superuser = True, **extra_fields)

class User(Model, AbstractBaseUser, PermissionsMixin):

	email_address = EmailField(
		max_length = 255,
		null = False,
		blank = False,
		unique = True,
		verbose_name = _('email address')
	)
	date_joined = DateTimeField(
		auto_now_add = True,
		verbose_name = _('date joined')
	)
	first_name = CharField(
		max_length = 64,
		null = False,
		blank = False,
		verbose_name = _('first name')
	)
	father_family_name = CharField(
		max_length = 64,
		blank = True,
		default = '',
		verbose_name = _('father\'s family name')
	)
	mother_family_name = CharField(
		max_length = 64,
		blank = True,
		default = '',
		verbose_name = _('mother\'s family name')
	)
	photo = ImageField(
		format = 'JPEG',
		spec_id = 'users:photo:spec',
		autoconvert = True,
		processors = [ ResizeToFill(240, 240) ],
		options = { 'quality': 80 },
		verbose_name = _('user photo')
	)
	campus = ForeignKey('fmfn.Campus',
		related_name = 'users',
		verbose_name = _('campus')
	)
	grades = ManyToManyField('fmfn.SchoolGrade',
		related_name = 'users',
		verbose_name = _('school grades')
	)
	role = ForeignKey('fmfn.Role',
		related_name = 'members',
		default = 1,
	    verbose_name = _('user role')
	)

	objects = UserManager()
	USERNAME_FIELD = 'email_address'
	REQUIRED_FIELDS = [
		'password',
		'first_name'
	]

	@property
	def is_active(self): return self.active
	@property
	def is_staff(self): return self.belongs_to(name = 'user manager')

	def get_full_name(self):

		family_name = ' '.join(filter(lambda i: bool(i), [ self.father_family_name or '', self.mother_family_name or '' ]))
		return ', '.join([ family_name, self.first_name ])

	def get_short_name(self): return self.first_name

	def belongs_to(self, name = None, **kwargs):

		def _belongs_recursive(role, target):

			if role == target: return True
			elif role.base is not None: return _belongs_recursive(role.base, target)
			else: return False

		target = Role.objects.active().get(name = name, **kwargs)
		return _belongs_recursive(self.role, target)

	class Meta(object):

		verbose_name = _('user')
		verbose_name_plural = _('users')
		app_label = 'fmfn'

class Role(Model):

	name = CharField(
		max_length = 64,
		null = False,
		blank = False,
		verbose_name = _('role name')
	)
	description = CharField(
		max_length = 512,
		null = False,
		default = '',
		verbose_name = _('role description')
	)
	base = ForeignKey('self',
		related_name = 'subroles',
		null = True,
	    verbose_name = _('base role')
	)
	base_permissions = ManyToManyField(Permission,
		related_name = 'roles',
		related_query_name = 'role',
		verbose_name = _('permissions')
	)

	@cached_property
	def permissions(self):

		query = self._get_permissions_query()
		return Permission.objects.filter(query)

	def _get_permissions_query(self, query = None):

		if query is None: query = Q(role__id = self.id)
		query = (query | self.role._get_permissions_query(query = query))

		return query

	def __str__(self): return self.name

	class Meta(object):

		verbose_name = _('user role')
		verbose_name_plural = _('user roles')
		app_label = 'fmfn'
