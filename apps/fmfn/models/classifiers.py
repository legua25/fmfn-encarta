# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from model_utils.managers import InheritanceManager
from django.db.models import *
from _base import Model, ActiveManager

class TagManager(ActiveManager, InheritanceManager): pass
class MaterialTag(Model):
	""" Represents a generic material tagging criteria. All material tags must, at least
		define the following:

			* name (CharField): A short, memorable name which serves as a search criteria.
			* materials (ForeignKey): A relationship to materials, in order to tag the material
			  with this tag.

		This model is abstract - it helps define new material tags, but cannot be created as-is.
	"""

	name = CharField(
		max_length = 64,
		verbose_name = _('type name')
	)

	materials = None

	objects = TagManager()

	class Meta(object):
		abstract = True

class Type(MaterialTag):
	""" Represents a tag describing types of materials: videos, documents, audio, etc. A material
		uses this tag to ease searching for materials of a certain type.
	"""

	materials = ManyToManyField('fmfn.Material',
		related_name = 'types',
		verbose_name = _('tagged materials')
	)

	class Meta(object):

		verbose_name = _('material type')
		verbose_name_plural = _('material types')
		app_label = 'fmfn'
class Theme(MaterialTag):
	""" Represents a tag describing a material theme: mathematics, linguistics, etc. A material uses
		this tag to ease searching for materials of a certain educational theme.
	"""

	materials = ManyToManyField('fmfn.Material',
		related_name = 'themes',
		verbose_name = _('tagged materials')
	)

	class Meta(object):

		verbose_name = _('material theme')
		verbose_name_plural = _('material themes')
		app_label = 'fmfn'
class Language(MaterialTag):
	""" Represents a tag describing a language in which written material is provided. A material uses
		this tag to ease searching for materials with content in a certain language.
	"""

	materials = ManyToManyField('fmfn.Material',
		related_name = 'languages',
		verbose_name = _('tagged materials')
	)

	class Meta(object):

		verbose_name = _('material language')
		verbose_name_plural = _('material languages')
		app_label = 'fmfn'
