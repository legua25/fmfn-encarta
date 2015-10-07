# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.forms import *

__all__ = [ 'CreateMaterialForm' ]

class CreateMaterialForm(Form):

	title = CharField(
		max_length = 1000,
		required = True,
		widget = TextInput(attrs = { 'placeholder': _('Title') })
	)
	description = CharField(
		max_length = 2000,
		required = False,
		widget = Textarea(attrs = { 'placeholder': _('Title') })
	)
	content = FileField(
		widget=FileInput()
	)
	link = URLField(
		widget=URLInput()
	)

