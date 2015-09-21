# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db.models import *
from material import *
from django.conf import settings

class Rating(Model):
	""" Represents the model for the rating. It contains:
			*rating_value(PositiveSmallIntegerField)): it has the rating value
			*material (ForeignKey): A relationship to materials in order to identify the rated material
			*user (ForeignKey): A relationship to users in order to know who rate the material
	"""

	rating_value = PositiveSmallIntegerField(
		choices = [
			(1, _('bad')),
			(2, _('regular')),
			(3, _('good')),
			(4, _('very good')),
			(5, _('excellent'))
		],
		verbose_name = _('rating values')
	)
	material = ForeignKey('fmfn.Material',
		related_name = 'ratings',
		verbose_name = _('material')
	)
	user = ForeignKey(settings.AUTH_USER_MODEL,
		related_name = '+',
		on_delete = CASCADE,

	)

	class Meta(object):

		verbose_name = _('rating')
		verbose_name_plural = _('ratings')
		app_label = 'fmfn'
