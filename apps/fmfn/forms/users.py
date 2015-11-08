# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from apps.fmfn.models import SchoolGrade, Role, Campus
from django.utils.crypto import constant_time_compare
from django.contrib.auth import get_user_model
from imagekit.processors import ResizeToFill
from django.forms import *
from imagekit.forms import ProcessedImageField as ImageField
from django.forms import ModelForm as Form

__all__ = [
	'UserCreationForm',
	'BasicEditForm',
	'AdminEditForm',
	'UserViewForm'
]
User = get_user_model()

class UserCreationForm(Form):

	password = CharField(
		max_length = 128,
		required = True,
		widget = PasswordInput(attrs = { 'placeholder': _('Contraseña') })
	)
	repeat = CharField(
		max_length = 128,
		required = True,
		widget = PasswordInput(attrs = { 'placeholder': _('Repita contraseña') })
	)
	role = ModelChoiceField(Role.objects.active(),
	    empty_label = None,
	    required = False,
	    widget = RadioSelect()
	)
	campus = ModelChoiceField(Campus.objects.active(),
	    empty_label = None,
	    required = True,
	    widget = Select()
	)

	def clean(self):

		Form.clean(self)

		password, repeat = self.cleaned_data['password'], self.cleaned_data['repeat']
		if not constant_time_compare(password, repeat): raise ValidationError('Las contraseñas no coinciden')

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
			'email_address': EmailInput(attrs = { 'placeholder': _('Correo electrónico') }),
			'first_name': TextInput(attrs = { 'placeholder': _('Nombre(s)') }),
			'father_family_name': TextInput(attrs = { 'placeholder': _('Apellido paterno') }),
			'mother_family_name': TextInput(attrs = { 'placeholder': _('Apellido Materno') }),
			'grades': CheckboxSelectMultiple(),
			'role': RadioSelect()
		}

class UserEditForm(Form):

	password = CharField(
		max_length = 128,
		required = True,
		widget = PasswordInput(attrs = { 'placeholder': _('Contraseña') })
	)
	repeat = CharField(
		max_length = 128,
		required = True,
		widget = PasswordInput(attrs = { 'placeholder': _('Repite la contraseña') })
	)

	is_managed = False

	def clean(self):

		Form.clean(self)

		password, repeat = self.cleaned_data['password'], self.cleaned_data['repeat']
		if not constant_time_compare(password, repeat): raise ValidationError('Las contraseñas no coinciden')

	class Meta(object):

		model = User
		fields = []
class BasicEditForm(UserEditForm):

	class Meta(object):

		model = User
		fields = [ 'photo' ]
class AdminEditForm(UserEditForm):

	role = ModelChoiceField(Role.objects.active(),
	    empty_label = None,
	    required = False,
	    widget = RadioSelect()
	)
	grades = ModelMultipleChoiceField(SchoolGrade.objects.active(),
		required = False,
		widget = CheckboxSelectMultiple()
	)

	is_managed = True

	class Meta(object):

		model = User
		fields = [
			'photo',
			'email_address',
			'first_name',
			'father_family_name',
			'mother_family_name',
			'campus',
			'role',
			'grades'
		]
		widgets = {
			'email_address': EmailInput(attrs = { 'placeholder': _('Correo electrónico') }),
			'first_name': TextInput(attrs = { 'placeholder': _('Nombre(s)') }),
			'father_family_name': TextInput(attrs = { 'placeholder': _('Apellido Paterno') }),
			'mother_family_name': TextInput(attrs = { 'placeholder': _('Apellido Materno') })
		}

class UserViewForm(Form):

	role = ModelChoiceField(Role.objects.active(),
	    empty_label = None,
	    required = False,
	    widget = RadioSelect()
	)
	grades = ModelMultipleChoiceField(SchoolGrade.objects.active(),
		required = False,
		widget = CheckboxSelectMultiple()
	)

	is_managed = True

	class Meta(object):

		model = User
		fields = [
			'photo',
			'email_address',
			'first_name',
			'father_family_name',
			'mother_family_name',
			'campus',
			'role',
			'grades'
		]
		widgets = {
			'email_address': EmailInput(attrs = { 'placeholder': _('Correo electrónico') }),
			'first_name': TextInput(attrs = { 'placeholder': _('Nombre(s)') }),
			'father_family_name': TextInput(attrs = { 'placeholder': _('Apellido Paterno') }),
			'mother_family_name': TextInput(attrs = { 'placeholder': _('Apellido Materno') })
		}
