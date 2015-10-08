# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.forms import *

__all__ = ['ProfileForm', 'AdminProfileForm']
User = get_user_model()

class ProfileForm(ModelForm):

	password = CharField(
		max_length = 128,
		required = True,
		widget = PasswordInput(attrs = { 'placeholder': _('Password') })
	)

	class Meta(object):
		model = User
		fields = [ 'email_address' ]

	def clean(self):

		Form.clean(self)

		password = self.cleaned_data['password']
		self.instance.set_password(password)

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
