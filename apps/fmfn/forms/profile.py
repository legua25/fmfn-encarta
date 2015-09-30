# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.forms import *
from apps.fmfn.models import profile

__all__ = ['ProfileForm']

class ProfileForm(Form):

	email_address = EmailField(
		widget = EmailInput(attrs = { 'placeholder': _('Email address') }),
		max_length= 255,
		required= True

	)

	password = CharField(
		widget= PasswordInput(attrs = { 'placeholder': _('password') }),
		max_length= 128,
		required= True
	)

	def __init__(self, user, *args, **kwargs):

		Form.__init__(self, *args, **kwargs)
		self._user = user
