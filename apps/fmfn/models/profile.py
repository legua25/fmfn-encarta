# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db.models import *
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from _base import Model

class Profile(Model):
	"""
		Fields firstname, lastname, email already present on AUTH_USER_MODEL
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
		app_label = 'fmfn'