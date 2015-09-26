# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate
from django.forms import *

__all__ = [ 'LoginForm' ]

class LoginForm(Form):

	email = EmailField(
		max_length = 255,
		required = True,
		widget = EmailInput(attrs = { 'placeholder': _('Email address') })
	)
	password = CharField(
		max_length = 128,
		required = True,
		widget = PasswordInput(attrs = { 'placeholder': _('Password') })
	)

	user = None

	def clean(self):

		# Obtain cleaned form data
		data = self.cleaned_data
		email, password = (data['email'], data['password'])

		# Attempt to authenticate the user
		user = authenticate(username = email, password = password)

		if user is not None:

			if user.is_active: self.user = user
			else: raise ValidationError('Requested user account is not active')
		else: raise ValidationError('Failed to authenticate user')
