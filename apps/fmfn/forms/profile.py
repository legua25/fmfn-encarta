# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.forms import *
from apps.fmfn.models import users

__all__ = ['ProfileForm']

class ProfileForm(ModelForm):

	class _Meta(object):
		model = users
		fields = ('email_address', 'password')

	def __init__(self, user, *args, **kwargs):

		Form.__init__(self, *args, **kwargs)
		self._user = user

class ProfileForm(ModelForm):

	class _Meta(object):
		model = users
		fields = ('first_name', 'last_name_father', 'last_name_mother','email_address', 'password')

	def __init__(self, user, *args, **kwargs):

		Form.__init__(self, *args, **kwargs)
		self._user = user