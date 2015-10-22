# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db.models import *
from _base import Model, ActiveManager

class PortfolioManager(ActiveManager):

	def user(self, user):

		try: return self.active().get(user = user)
		except Portfolio.DoesNotExist: return self.create(user = user)
class Portfolio(Model):
	"""" Registry of materials marked as favorite by a user
	"""

	user = ForeignKey(settings.AUTH_USER_MODEL,
        related_name = 'portfolio',
        verbose_name = _('user')
    )

	objects = PortfolioManager()

	class Meta(object):

		verbose_name = _('portfolio')
		verbose_name_plural = _('portfolios')
		app_label = 'fmfn'

class Item(Model):

	portfolio = ForeignKey('fmfn.Portfolio',
	    related_name = 'items',
	    verbose_name = _('portfolio items')
	)
	material = ForeignKey('fmfn.Material',
		related_name = '+',
	    verbose_name = _('material')
	)
	date_added = DateTimeField(
		auto_now_add = True,
		verbose_name = _('date added')
	)

	class Meta(object):

		verbose_name = _('portfolio item')
		verbose_name_plural = _('portfolio items')
		app_label = 'fmfn'
