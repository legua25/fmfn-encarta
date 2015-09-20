# -*- coding: utf-8 -*-
from django.db.models import *

class MaterialTag(Model):

	name = CharField(
		max_length = 64,
		verbose_name = _('type name')
	)
	description = CharField(
		max_length = 256,
		verbose_name = _('type description')
	)
	materials = ForeignKey('fmfn.Material',
		related_name = 'themes',
		on_delete = CASCADE,
		verbose_name = _('tagged materials')
	)

	class Meta(object):
		abstract = True

class Type(MaterialTag):

	class Meta(object):

		verbose_name = _('material type')
		verbose_name_plural = _('material types')
		app_label = 'fmfn'
class Theme(MaterialTag):

	class Meta(object):

		verbose_name = _('material type')
		verbose_name_plural = _('material types')
		app_label = 'fmfn'
class Language(MaterialTag):

	class Meta(object):

		verbose_name = _('material language')
		verbose_name_plural = _('material languages')
		app_label = 'fmfn'
