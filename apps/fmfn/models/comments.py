# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db.models import *
from django.conf import settings
from _base import Model

class Comment(Model):

	user = ForeignKey(
		settings.AUTH_USER_MODEL,
		related_name = 'comments',
		verbose_name = _('author')
	)

	comment_text = CharField(
		max_length = 64
	)

	material = ForeignKey('fmfn.Material',
		related_name = 'comments',
		verbose_name = _('material')
	)


	class Meta(object):
		verbose_name = _('material_comment')
		verbose_name_plural = _('material_comments')
		app_label = 'fmfn'
