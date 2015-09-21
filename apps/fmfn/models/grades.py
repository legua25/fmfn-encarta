# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db.models import *
from _base import Model

class Grade(Model):

	name = CharField(
		max_length = 64,
		verbose_name = _('name')
	)
	min_age = PositiveSmallIntegerField(verbose_name = _('minimum expected age'))
	max_age = PositiveSmallIntegerField(verbose_name = _('maximum expected age'))

	class Meta(object):

		verbose_name = _('school grade')
		verbose_name_plural = _('school grades')
		app_label = 'fmfn'
