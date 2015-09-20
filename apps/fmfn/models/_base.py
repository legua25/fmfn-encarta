# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db.models import Model as BaseModel
from django.db.models import *

__all__ = [ 'Model' ]

class ActiveManager(Manager):

	def inactive(self): return self.filter(active = False)
	def active(self): return self.filter(active = True)

class Model(BaseModel):

	active = BooleanField(
		default = True,
		verbose_name = _('is active')
	)

	objects = ActiveManager()

	def delete(self, soft = True, using = None):

		if soft is True:

			self.active = False
			self.save(using = using)
		else: Model.delete(self, using = using)

	class Meta(object):
		abstract = True
