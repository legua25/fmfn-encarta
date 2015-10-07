# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from apps.fmfn.models import Material
from django.forms import *
from django.forms import ModelForm as Form

__all__ = [ 'MaterialForm' ]

class MaterialForm(Form):

	class Meta(object):

		model = Material
		fields = [
			'title',
			'content',
			'link',
			'description',
			'suggested_ages'
		]
		widgets = {
			'title': TextInput(attrs = { 'placeholder': _('Title') }),
			'link': URLInput(attrs = { 'placeholder': _('Content link (optional)') }),
			'description': Textarea(attrs = { 'placeholder': _('Description') }),
			'suggested_ages': CheckboxSelectMultiple()
		}
