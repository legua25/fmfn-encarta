# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group as Role
from imagekit.processors import ResizeToFill
from apps.fmfn.models import Grade
from django.forms import *
from imagekit.forms import ProcessedImageField as ImageField

__all__ = [ 'UserForm' ]

class UserForm(Form):

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
	repeat = CharField(
		max_length = 128,
		required = True,
		widget = PasswordInput(attrs = { 'placeholder': _('Repeat password') })
	)

	first_name = CharField(
		max_length = 128,
		required = True,
		widget = TextInput(attrs = { 'placeholder': _('First name') })
	)
	family_name = CharField(
		max_length = 256,
		required = True,
		widget = TextInput(attrs = { 'placeholder': _('Family name') })
	)
	campus = ChoiceField(
		choices = [
			('none', _('Select campus'))
		],
		initial = 'none',
		required = True
	)
	grades = ModelMultipleChoiceField(
		queryset = Grade.objects.active(),
		required = False,
		widget = CheckboxSelectMultiple()
	)
	photo = ImageField(
		format = 'JPEG',
		spec_id = 'users:photo:spec',
		autoconvert = True,
		processors = [ ResizeToFill(240, 240) ],
		options = { 'quality': 80 },
		required = False
	)
	role = ModelChoiceField(
		queryset = Role.objects.all(),
		required = True,
		widget = RadioSelect()
	)

	def __init__(self, user = None, *args, **kwargs):

		Form.__init__(self, *args, **kwargs)
		self.user = user
