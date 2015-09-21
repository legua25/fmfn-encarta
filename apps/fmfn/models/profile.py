# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db.models import *
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from _base import Model

class Profile(Model):
	"""
		Represents the model for the user, note that the fields firstname, lastname, email are already present on the AUTH_USER_MODEL referenced on the user foreign key
		*user(ForeignKeyField): Reference to the django default user model
		*campus(CharField): The campus this user is registered on
		*class_grades(ManyToManyField): The grades this user teaches on
	"""

	user = ForeignKey(settings.AUTH_USER_MODEL,
		related_name = 'profile',
		verbose_name = _('user')
	)
	campus = CharField(
		max_length=64,
		verbose_name = _('campus'),
		null = True
	)
	class_grades = ManyToManyField('fmfn.Grade',
		related_name = '+',
		verbose_name = _('class grades')
	)

	class Meta(object):

		verbose_name = _('user profile')
		verbose_name_plural = _('user profiles')
		app_label = 'fmfn'
