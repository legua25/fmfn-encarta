# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_str
from django.db.models import *
from _base import Model

class Campus(Model):

	name = CharField(
		max_length = 256,
		null = False,
		blank = False,
		verbose_name = _('campus name')
	)
	date_added = DateTimeField(
		auto_now_add = True,
		verbose_name = _('date added')
	)

	def __str__(self): return smart_str(self.name)

	class Meta(object):

		verbose_name = _('campus')
		verbose_name_plural = _('campi')
		app_label = 'fmfn'
class SchoolGrade(Model):
	"""
		Represents the school grades used by other models:

        * name (CharField): The name of the school grade
        * min_age (PositiveSmallIntegerField): The minimum age that is related to this grade
        * max_age (PositiveSmallIntegerField): The maximum age that is related to this grade
	"""

	name = CharField(
		max_length = 64,
		verbose_name = _('name')
	)
	min_age = PositiveSmallIntegerField(verbose_name = _('minimum expected age'))
	max_age = PositiveSmallIntegerField(verbose_name = _('maximum expected age'))

	def __str__(self): return smart_str(self.name)

	class Meta(object):

		verbose_name = _('school grade')
		verbose_name_plural = _('school grades')
		app_label = 'fmfn'
