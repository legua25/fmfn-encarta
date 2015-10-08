# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.utils.crypto import constant_time_compare
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from django.forms import *

__all__ = [ 'UserEditForm', 'AdminProfileForm' ]
User = get_user_model()

class UserEditForm(ModelForm):

	password = CharField(
		max_length = 128,
		required = True,
		widget = PasswordInput(attrs = { 'placeholder': _('Password') })
	)
	repeat = CharField(
		max_length = 128,
		required = True,
		widget = PasswordInput(attrs = { 'placeholder': _('Repeat password') })
	)

	def clean(self):

		ModelForm.clean(self)
		password, repeat = self.cleaned_data['password'], self.cleaned_data['repeat']

		if self.user is not None:
			if constant_time_compare(password, repeat): self.user.set_password(password)
			else: raise ValidationError(_('Passwords did not match'))

		else: raise ValidationError(_('Invalid user account'))

	class Meta(object):
		model = User
		fields = [ 'email_address' ]

class AdminProfileForm(ModelForm):

	password = CharField(
		max_length = 128,
		required = True,
		widget = PasswordInput(attrs = { 'placeholder': _('Password') })
	)
	repeat = CharField(
		max_length = 128,
		required = True,
		widget = PasswordInput(attrs = { 'placeholder': _('Repeat password') })
	)

	def clean(self):

		ModelForm.clean(self)
		password, repeat = self.cleaned_data['password'], self.cleaned_data['repeat']

		if self.user is not None:
			if constant_time_compare(password, repeat): self.user.set_password(password)
			else: raise ValidationError(_('Passwords did not match'))

		else: raise ValidationError(_('Invalid user account'))

	class Meta(object):
		model = User
		fields = [
			'first_name',
			'father_family_name',
			'mother_family_name',
			'email_address',
			'photo',
			'grades',
			'campus',
			'role'
		]
