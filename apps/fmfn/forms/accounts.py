# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import authenticate
from django.forms import *

__all__ = [ 'LoginForm', 'RecoveryForm' ]

class LoginForm(Form):

	email_address = EmailField(
		max_length = 255,
		required = True,
		widget = EmailInput(attrs = { 'placeholder': _('Email address') })
	)
	password = CharField(
		max_length = 128,
		required = True,
		widget = PasswordInput(attrs = { 'placeholder': _('Password') })
	)
	user = AnonymousUser()

	def clean(self):

		email, password = (self.cleaned_data['email_address'], self.cleaned_data['password'])
		user = authenticate(username = email, password = password)

		if user is not None:

			if user.is_active: self.user = user
			else: raise ValidationError(_('Requested user is no longer active on this site'))

		else: raise ValidationError(_('Email address and/or password did not match.'))

class RecoveryForm(Form):

	email_address = None
	password = None
	repeat = None

	def __init__(self, *args, **kwargs):

		self.user = kwargs.pop('user', AnonymousUser())
		self._stage = stage = kwargs.pop('stage', '')

		if stage == 'recover':

			self.email_address = EmailField(
				max_length = 255,
				required = True,
				widget = EmailInput(attrs = { 'placeholder': _('Email address') })
			)
		elif stage == 'complete':

			self.password = CharField(
				max_length = 128,
				required = True,
				widget = PasswordInput(attrs = { 'placeholder': _('Password') })
			)
			self.repeat = CharField(
				max_length = 128,
				required = True,
				widget = PasswordInput(attrs = { 'placeholder': _('Password') })
			)
		else: raise ValueError('Invalid value for stage (expected: "recover" or "complete", received: %s)' % stage)

		Form.__init__(self, *args, **kwargs)

	def clean(self):
		pass
