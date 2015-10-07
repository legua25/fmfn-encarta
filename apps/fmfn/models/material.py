# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db.models import *
from _base import Model
from uuid import uuid4

def upload_to(instance, filename):

	name, ext = filename.rsplit('.', 1)
	return '%s-%s.%s' % (name, uuid4().hex, ext)

class Material(Model):
	""" Represents the model for the materials. It contains:
		*title(CharField): it's the title of the material
		*description(Charfield): it's the description of the material
		*suggested_ages(PositiveSmallIntegerField): the optional values here are related with the educational level
		*user (ForeignKey): A relationship to users to know if the material is visible to them
	"""

	title = CharField(
		max_length = 128,
		null = False,
		blank = False,
		verbose_name = _('title')
	)
	content = FileField(
		null = True,
		blank = True,
		upload_to = upload_to,
		verbose_name = _('content file')
	)
	link = URLField(
		null = True,
		blank = True,
		verbose_name = _('content link')
	)
	description = CharField(
		max_length = 1024,
		null = False,
		blank = False,
		verbose_name = _('description')
	)
	suggested_ages = ManyToManyField('fmfn.SchoolGrade',
		related_name = 'materials',
		verbose_name = _('suggested ages')
	)
	user = ForeignKey(settings.AUTH_USER_MODEL,
		related_name = 'materials',
		verbose_name = _('uploading user')
	)

	class Meta(object):

		verbose_name = _('material')
		verbose_name_plural = _('materials')
		app_label = 'fmfn'
