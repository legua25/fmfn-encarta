# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db.models import *
from _base import Model

class MaterialTag(Model):

	name = CharField(
		max_length = 64,
		verbose_name = _('type name')
	)
	description = CharField(
		max_length = 256,
		verbose_name = _('type description')
	)
	materials = None

	class Meta(object):
		abstract = True

class Type(MaterialTag):

	materials = ForeignKey('fmfn.Material',
		related_name = 'types',
		on_delete = CASCADE,
		verbose_name = _('tagged materials')
	)

	class Meta(object):

		verbose_name = _('material type')
		verbose_name_plural = _('material types')
		app_label = 'fmfn'
class Theme(MaterialTag):

	materials = ForeignKey('fmfn.Material',
		related_name = 'themes',
		on_delete = CASCADE,
		verbose_name = _('tagged materials')
	)

	class Meta(object):

		verbose_name = _('material type')
		verbose_name_plural = _('material types')
		app_label = 'fmfn'
class Language(MaterialTag):

	materials = ForeignKey('fmfn.Material',
		related_name = 'languages',
		on_delete = CASCADE,
		verbose_name = _('tagged materials')
	)

	class Meta(object):

		verbose_name = _('material language')
		verbose_name_plural = _('material languages')
		app_label = 'fmfn'
