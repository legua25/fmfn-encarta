# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db.models import *
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

class Profile(Model):

	user = ForeignKey(settings.AUTH_USER_MODEL,
		related_name = 'profile',
		verbose_name = _('user')
	)

	class Meta(object):
		app_label = 'fmfn'