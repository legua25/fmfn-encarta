# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from apps.fmfn.models import User
from django.db.models import *
from _base import Model, ActiveManager
from django.conf import settings

class PortfolioManager(ActiveManager):

	def user(self, user):

		try: return self.active().get(user = user)
		except Portfolio.DoesNotExist: return self.create(user = user)
class Portfolio(Model):
	"""" Registry of materials marked as favorite by a user
	"""

	materials = ManyToManyField('fmfn.Material',
        related_name = '+',
        verbose_name = _('materials')
    )
	user = ForeignKey(settings.AUTH_USER_MODEL,
        related_name = 'portfolio',
        verbose_name = _('user')
    )
	date_added = DateTimeField(
		auto_now_add = True,
		verbose_name = _('date added')
	)

	objects = PortfolioManager()

	class Meta(object):

		verbose_name = _('portfolio')
		verbose_name_plural = _('portfolios')
		app_label = 'fmfn'
