# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db.models import *
from material import *
from django.conf import settings

class Rating(Model):

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
		null = False,
		verbose_name = _('material')
	)
	user = ForeignKey(settings.AUTH_USER_MODEL,
		null = False,
		on_delete = CASCADE
	)

	class Meta(object):

		verbose_name = _('rating')
		verbose_name_plural = _('ratings')
		app_label = 'fmfn'