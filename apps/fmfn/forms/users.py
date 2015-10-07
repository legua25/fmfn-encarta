# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.utils.crypto import constant_time_compare
from django.contrib.auth import get_user_model
from apps.fmfn.models import SchoolGrade, Role
from imagekit.processors import ResizeToFill
from django.forms import *
from imagekit.forms import ProcessedImageField as ImageField
from django.forms import ModelForm as Form

__all__ = ['UserCreationForm']
User = get_user_model()

class UserCreationForm(Form):

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

	def clear(self):

		Form.clear(self)

		password, repeat = self.cleaned_data['password'], self.cleaned_data['repeat']
		if not constant_time_compare(password, repeat): raise ValidationError('Passwords do not match')

	class Meta(object):

		model = User
		fields = [
			'email_address',
			'first_name',
			'father_family_name',
			'mother_family_name',
			'photo',
			'campus',
			'grades',
			'role'
		]
		widgets = {
			'email_address': EmailInput(attrs = { 'placeholder': _('Email address') }),
			'first_name': TextInput(attrs = { 'placeholder': _('First name') }),
			'father_family_name': TextInput(attrs = { 'placeholder': _('Father\'s family name') }),
			'mother_family_name': TextInput(attrs = { 'placeholder': _('Mother\'s family name') }),
			'grades': CheckboxSelectMultiple(),
			'role': RadioSelect()
		}
