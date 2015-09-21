# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db.models import *
from django.conf import settings
from _base import Model

class Comment(Model):
	"""
    Represents a user's comment on a particular material. Each comment defines:

        * user (ForeignKey): A reference to the user that posted the comment
        * description (CharField): The message content of the comment
        * material (ForeignKey): A reference to the material that is being commented
        * date_created (ForeignKey): A timestamp of the date that the comment was posted
    """

	user = ForeignKey(
		settings.AUTH_USER_MODEL,
		related_name = 'comments',
		verbose_name = _('author')
	)
	content = CharField(
		max_length = 64,
		verbose_name = _('comment content')
	)
	date_created = DateTimeField(
		auto_now_add = True,
		verbose_name = _('date created')
	)
	material = ForeignKey('fmfn.Material',
		related_name = 'comments',
		verbose_name = _('commented material')
	)

	class Meta(object):

		verbose_name = _('material comment')
		verbose_name_plural = _('material comments')
		app_label = 'fmfn'
