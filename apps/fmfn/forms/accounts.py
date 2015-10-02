# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import authenticate
from django.forms import *

__all__ = [ 'LoginForm' ]

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
