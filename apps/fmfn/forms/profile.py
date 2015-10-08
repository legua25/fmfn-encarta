# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.utils.crypto import constant_time_compare
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from django.forms import *

__all__ = ['ProfileForm', 'AdminProfileForm', 'PasswordForm']
User = get_user_model()

class PasswordForm(Form):

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

	def __init__(self, *args, **kwargs):

		user = kwargs.pop('user', AnonymousUser())

		Form.__init__(self, *args, **kwargs)
		self.user = user

	def clean(self):

		password, repeat = self.cleaned_data['password'], self.cleaned_data['repeat']

		if self.user is not None:
			if constant_time_compare(password, repeat): self.user.set_password(password)
			else: raise ValidationError(_('Passwords did not match'))

		else: raise ValidationError(_('Invalid user account'))


class ProfileForm(ModelForm):

	class Meta(object):
		model = User
		fields = [ 'email_address' ]

class AdminProfileForm(ModelForm):

	password = CharField(
		max_length = 128,
		required = True,
		widget = PasswordInput(attrs = { 'placeholder': _('Password') })
	)

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


	def clean(self):

		Form.clean(self)

		password = self.cleaned_data['password']
		self.instance.set_password(password)
